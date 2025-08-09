"""Command line tool to log KuCoin Futures balances."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from filelock import FileLock

import requests
import yaml
import frontmatter
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class Config:
    """Runtime configuration for balance logging."""

    api_key: str
    api_secret: str
    api_passphrase: str
    currency: str = "USDT"
    vault_path: str = ""
    balance_folder: str = "Trading/Balances/KuCoin"
    cache_file: str = field(
        default_factory=lambda: os.path.expanduser("~/.kucoin_balance_log.json")
    )
    api_timeout: float = 10.0
    api_max_retries: int = 3
    api_retry_wait: float = 1.0
    today: str = field(
        default_factory=lambda: datetime.today().strftime("%Y-%m-%d")
    )


logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure application wide logging."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def load_config() -> Config:
    """Load configuration from environment variables."""

    load_dotenv()
    api_key = os.getenv("KUCOIN_API_KEY", "")
    api_secret = os.getenv("KUCOIN_API_SECRET", "")
    api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE", "")
    currency = os.getenv("KUCOIN_BALANCE_CURRENCY", "USDT")
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "")
    balance_folder = os.getenv("BALANCE_FOLDER", "Trading/Balances/KuCoin")
    cache_file = os.path.expanduser(
        os.getenv("BALANCE_CACHE_FILE", "~/.kucoin_balance_log.json")
    )
    api_timeout = float(os.getenv("KUCOIN_API_TIMEOUT", "10"))
    api_max_retries = int(os.getenv("KUCOIN_API_MAX_RETRIES", "3"))
    api_retry_wait = float(os.getenv("KUCOIN_API_RETRY_WAIT", "1"))

    required_env = {
        "KUCOIN_API_KEY": api_key,
        "KUCOIN_API_SECRET": api_secret,
        "KUCOIN_API_PASSPHRASE": api_passphrase,
        "OBSIDIAN_VAULT_PATH": vault_path,
    }
    missing = [name for name, value in required_env.items() if not value]
    if missing:
        raise SystemExit(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    return Config(
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        currency=currency,
        vault_path=vault_path,
        balance_folder=balance_folder,
        cache_file=cache_file,
        api_timeout=api_timeout,
        api_max_retries=api_max_retries,
        api_retry_wait=api_retry_wait,
    )


# ---------------------------------------------------------------------------
# KuCoin API helpers
# ---------------------------------------------------------------------------


def kucoin_futures_headers(config: Config, endpoint: str, method: str = "GET") -> dict[str, str]:
    """Create authenticated headers for the KuCoin Futures API."""

    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}{method}{endpoint}"
    signature = base64.b64encode(
        hmac.new(config.api_secret.encode(), str_to_sign.encode(), hashlib.sha256).digest()
    ).decode()
    passphrase = base64.b64encode(
        hmac.new(config.api_secret.encode(), config.api_passphrase.encode(), hashlib.sha256).digest()
    ).decode()
    return {
        "KC-API-KEY": config.api_key,
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json",
    }


def fetch_futures_balance(config: Config) -> float:
    """Retrieve the current futures account equity for ``config.currency``."""

    endpoint = f"/api/v1/account-overview?currency={config.currency}"
    url = "https://api-futures.kucoin.com" + endpoint
    headers = kucoin_futures_headers(config, endpoint)
    with requests.Session() as session:
        for attempt in range(1, config.api_max_retries + 1):
            try:
                res = session.get(url, headers=headers, timeout=config.api_timeout)
                res.raise_for_status()
                try:
                    data = res.json()
                    return float(data["data"]["accountEquity"])
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
                    logger.error("Failed to parse JSON response: %s", e)
                    raise RuntimeError(f"Failed to parse JSON: {e}") from e
            except requests.exceptions.RequestException as e:
                if attempt < config.api_max_retries:
                    wait_time = config.api_retry_wait * (2 ** (attempt - 1))
                    logger.warning(
                        "Request failed (attempt %s/%s): %s",
                        attempt,
                        config.api_max_retries,
                        e,
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        "Failed to fetch balance after %s attempts: %s",
                        config.api_max_retries,
                        e,
                    )
                    raise RuntimeError(f"Failed to fetch balance: {e}") from e


# ---------------------------------------------------------------------------
# Vault file helpers
# ---------------------------------------------------------------------------


def read_previous_balance(config: Config, date_str: str) -> float:
    """Read the balance for the day before ``date_str`` from the vault."""

    prev_date = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    file_path = os.path.join(config.vault_path, config.balance_folder, f"{prev_date}.md")
    if not os.path.exists(file_path):
        logger.info("🆕 No data for %s — creating placeholder.", prev_date)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(f"---\ndate: {prev_date}\nbalance: 0.00\n---\n")
        return 0.00
    with open(file_path, "r") as f:
        content = f.read()
    try:
        post = frontmatter.loads(content)
        if not post.metadata:
            raise yaml.YAMLError("missing or malformed front matter")
        return float(post.metadata.get("balance", 0.00))
    except (yaml.YAMLError, ValueError, TypeError, AttributeError) as e:
        logger.warning("Failed to parse balance file %s: %s", file_path, e)
        return 0.00
    except Exception as e:
        logger.exception("Unexpected error reading balance file %s: %s", file_path, e)
        raise


def write_balance(config: Config, date_str: str, balance: float) -> None:
    """Write ``balance`` for ``date_str`` to the vault markdown file."""

    file_path = os.path.join(config.vault_path, config.balance_folder, f"{date_str}.md")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(f"---\ndate: {date_str}\nbalance: {balance:.2f}\n---\n")
    logger.info("✅ Logged balance for %s: %.2f", date_str, balance)


# ---------------------------------------------------------------------------
# Cache control
# ---------------------------------------------------------------------------


def already_logged(config: Config, date_str: str) -> bool:
    """Return ``True`` if ``date_str`` has already been logged today."""

    if date_str != config.today:
        return False
    lock = FileLock(config.cache_file + ".lock")
    with lock:
        if not os.path.exists(config.cache_file):
            return False
        try:
            with open(config.cache_file, "r") as f:
                data = json.load(f)
            return data.get("last_logged_date") == date_str
        except (OSError, json.JSONDecodeError, AttributeError) as e:
            logger.warning("Failed to read cache file %s: %s", config.cache_file, e)
            return False
        except Exception as e:
            logger.exception(
                "Unexpected error accessing cache file %s: %s", config.cache_file, e
            )
            raise


def mark_logged(config: Config, date_str: str) -> None:
    """Record in the cache file that ``date_str`` has been logged."""

    if date_str != config.today:
        return
    lock = FileLock(config.cache_file + ".lock")
    with lock:
        cache_dir = os.path.dirname(config.cache_file) or "."
        os.makedirs(cache_dir, exist_ok=True)
        tmp_file = config.cache_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump({"last_logged_date": date_str}, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file, config.cache_file)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> None:
    """Command line entry point for balance logging."""

    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Override date for backfill (YYYY-MM-DD)")
    parser.add_argument("--cache-file", help="Override cache file location")
    args = parser.parse_args(argv)

    config = load_config()
    if args.cache_file:
        config.cache_file = os.path.expanduser(args.cache_file)

    target_date = args.date if args.date else config.today

    if already_logged(config, target_date):
        logger.warning("🟡 Already logged today — skipping.")
        return

    try:
        balance = fetch_futures_balance(config)
        previous_balance = read_previous_balance(config, target_date)
        write_balance(config, target_date, balance)
        mark_logged(config, target_date)

        change = balance - previous_balance
        pct = (change / previous_balance) * 100 if previous_balance != 0 else 0
        symbol = "📈" if change > 0 else "📉" if change < 0 else "🔁"
        logger.info(
            "%s Change since previous day: %+0.2f (%+0.2f%%)",
            symbol,
            change,
            pct,
        )
    except Exception as e:
        logger.exception("❌ Error: %s", e)
        raise


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()


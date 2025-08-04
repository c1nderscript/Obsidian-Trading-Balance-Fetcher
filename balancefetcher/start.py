import requests
import base64
import hashlib
import hmac
import time
import os
import json
import argparse
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import yaml

# === Logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# === Load config ===
load_dotenv()

api_key = os.getenv("KUCOIN_API_KEY")
api_secret = os.getenv("KUCOIN_API_SECRET")
api_passphrase = os.getenv("KUCOIN_API_PASSPHRASE")
currency = os.getenv("KUCOIN_BALANCE_CURRENCY", "USDT")
vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
balance_folder = os.getenv("BALANCE_FOLDER", "Trading/Balances/KuCoin")
cache_file = os.path.expanduser("~/.kucoin_balance_log.json")
api_timeout = float(os.getenv("KUCOIN_API_TIMEOUT", "10"))

# Ensure all required environment variables are present
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

# === CLI args ===
parser = argparse.ArgumentParser()
parser.add_argument("--date", help="Override date for backfill (YYYY-MM-DD)")
args = parser.parse_args()

today = datetime.today().strftime("%Y-%m-%d")
target_date = args.date if args.date else today

# === KuCoin auth ===
def kucoin_futures_headers(endpoint, method="GET"):
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}{method}{endpoint}"
    signature = base64.b64encode(
        hmac.new(api_secret.encode(), str_to_sign.encode(), hashlib.sha256).digest()
    ).decode()
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode(), api_passphrase.encode(), hashlib.sha256).digest()
    ).decode()
    return {
        "KC-API-KEY": api_key,
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": now,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json"
    }

# === Fetch balance from KuCoin Futures ===
def fetch_futures_balance(currency="USDT"):
    endpoint = f"/api/v1/account-overview?currency={currency}"
    url = "https://api-futures.kucoin.com" + endpoint
    headers = kucoin_futures_headers(endpoint)
    res = requests.get(url, headers=headers, timeout=api_timeout)
    res.raise_for_status()
    return float(res.json()["data"]["accountEquity"])

# === Read previous day's balance ===
def read_previous_balance(date_str: str):
    prev_date = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    file_path = os.path.join(vault_path, balance_folder, f"{prev_date}.md")
    if not os.path.exists(file_path):
        logger.info("🆕 No data for %s — creating placeholder.", prev_date)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(f"---\ndate: {prev_date}\nbalance: 0.00\n---\n")
        return 0.00
    with open(file_path, "r") as f:
        try:
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                yaml_content = parts[1] if len(parts) > 1 else content
            else:
                yaml_content = content
            data = yaml.safe_load(yaml_content) or {}
            return float(data.get("balance", 0.00))
        except Exception:
            return 0.00

# === Write balance for a specific date ===
def write_balance(date_str: str, balance: float):
    file_path = os.path.join(vault_path, balance_folder, f"{date_str}.md")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(f"---\ndate: {date_str}\nbalance: {balance:.2f}\n---\n")
    logger.info("✅ Logged balance for %s: %.2f", date_str, balance)

# === Cache control ===
def already_logged(date_str: str) -> bool:
    if date_str != today:
        return False
    if not os.path.exists(cache_file):
        return False
    try:
        with open(cache_file, "r") as f:
            data = json.load(f)
        return data.get("last_logged_date") == date_str
    except:
        return False

def mark_logged(date_str: str):
    if date_str != today:
        return
    with open(cache_file, "w") as f:
        json.dump({"last_logged_date": date_str}, f)

# === Main ===
if __name__ == "__main__":
    if already_logged(target_date):
        logger.warning("🟡 Already logged today — skipping.")
        exit(0)

    try:
        balance = fetch_futures_balance(currency)
        previous_balance = read_previous_balance(target_date)
        write_balance(target_date, balance)
        mark_logged(target_date)

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


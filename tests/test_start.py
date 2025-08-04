import os
import sys
from pathlib import Path
import importlib.util
import logging
import requests
import pytest

# Ensure required env vars exist before importing module
os.environ.setdefault("KUCOIN_API_KEY", "testkey")
os.environ.setdefault("KUCOIN_API_SECRET", "testsecret")
os.environ.setdefault("KUCOIN_API_PASSPHRASE", "testpass")
os.environ.setdefault("OBSIDIAN_VAULT_PATH", "/tmp")

# Prevent argparse in start.py from parsing pytest arguments
sys.argv = ["start.py"]

spec = importlib.util.spec_from_file_location(
    "start", Path(__file__).resolve().parent.parent / "balancefetcher" / "start.py"
)
start = importlib.util.module_from_spec(spec)
spec.loader.exec_module(start)


def test_fetch_futures_balance(monkeypatch):
    class MockResponse:
        def json(self):
            return {"data": {"accountEquity": "123.45"}}

        def raise_for_status(self):
            pass

    def mock_get(url, headers, timeout=None):
        return MockResponse()

    monkeypatch.setattr(start.requests, "get", mock_get)
    assert start.fetch_futures_balance("USDT") == 123.45


def test_fetch_futures_balance_retries(monkeypatch):
    class MockResponse:
        def json(self):
            return {"data": {"accountEquity": "123.45"}}

        def raise_for_status(self):
            pass

    attempts = {"n": 0}

    def mock_get(url, headers, timeout=None):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise requests.exceptions.ConnectionError("boom")
        return MockResponse()

    monkeypatch.setattr(start.requests, "get", mock_get)
    monkeypatch.setattr(start, "api_max_retries", 3)
    monkeypatch.setattr(start, "api_retry_wait", 0)
    monkeypatch.setattr(start.time, "sleep", lambda s: None)
    assert start.fetch_futures_balance("USDT") == 123.45
    assert attempts["n"] == 3


def test_fetch_futures_balance_retries_fail(monkeypatch):
    def mock_get(url, headers, timeout=None):
        raise requests.exceptions.Timeout("timeout")

    monkeypatch.setattr(start.requests, "get", mock_get)
    monkeypatch.setattr(start, "api_max_retries", 2)
    monkeypatch.setattr(start, "api_retry_wait", 0)
    monkeypatch.setattr(start.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError):
        start.fetch_futures_balance("USDT")


def test_write_and_read_balance(tmp_path, monkeypatch):
    monkeypatch.setattr(start, "vault_path", str(tmp_path))
    date = "2024-01-01"
    start.write_balance(date, 123.45)
    file_path = tmp_path / start.balance_folder / f"{date}.md"
    assert file_path.exists()
    assert "balance: 123.45" in file_path.read_text()
    # Read previous day's balance
    assert start.read_previous_balance("2024-01-02") == 123.45


def test_read_previous_balance_creates_placeholder(tmp_path, monkeypatch):
    monkeypatch.setattr(start, "vault_path", str(tmp_path))
    balance = start.read_previous_balance("2024-01-02")
    placeholder = tmp_path / start.balance_folder / "2024-01-01.md"
    assert balance == 0.0
    assert placeholder.exists()
    assert "balance: 0.00" in placeholder.read_text()


def test_mark_and_already_logged(tmp_path, monkeypatch):
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr(start, "cache_file", str(cache_file))
    monkeypatch.setattr(start, "today", "2024-01-01")
    assert not start.already_logged("2024-01-01")
    start.mark_logged("2024-01-01")
    assert start.already_logged("2024-01-01")


def test_read_previous_balance_invalid_yaml(tmp_path, monkeypatch, caplog):
    monkeypatch.setattr(start, "vault_path", str(tmp_path))
    prev_date = "2024-01-01"
    file_path = tmp_path / start.balance_folder / f"{prev_date}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("---\n::not_yaml")
    with caplog.at_level(logging.WARNING):
        balance = start.read_previous_balance("2024-01-02")
    assert balance == 0.0
    assert "Failed to parse balance file" in caplog.text


def test_already_logged_invalid_json(tmp_path, monkeypatch, caplog):
    cache_file = tmp_path / "cache.json"
    cache_file.write_text("not-json")
    monkeypatch.setattr(start, "cache_file", str(cache_file))
    monkeypatch.setattr(start, "today", "2024-01-01")
    with caplog.at_level(logging.WARNING):
        assert not start.already_logged("2024-01-01")
    assert "Failed to read cache file" in caplog.text

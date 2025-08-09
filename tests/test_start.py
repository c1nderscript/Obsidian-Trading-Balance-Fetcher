import os
import sys
from pathlib import Path
import importlib.util
import logging
import json
import requests
import pytest

# Load the start module without executing the CLI entry point
sys.argv = ["start.py"]
spec = importlib.util.spec_from_file_location(
    "start", Path(__file__).resolve().parent.parent / "balancefetcher" / "start.py"
)
start = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = start
spec.loader.exec_module(start)


@pytest.fixture
def config(tmp_path):
    return start.Config(
        api_key="testkey",
        api_secret="testsecret",
        api_passphrase="testpass",
        vault_path=str(tmp_path),
        cache_file=str(tmp_path / "cache.json"),
    )


def test_fetch_futures_balance(monkeypatch, config):
    class MockResponse:
        def json(self):
            return {"data": {"accountEquity": "123.45"}}

        def raise_for_status(self):
            pass

    class MockSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def get(self, url, headers=None, timeout=None):
            return MockResponse()

    monkeypatch.setattr(start.requests, "Session", lambda: MockSession())
    assert start.fetch_futures_balance(config) == 123.45


def test_fetch_futures_balance_retries(monkeypatch, config):
    class MockResponse:
        def json(self):
            return {"data": {"accountEquity": "123.45"}}

        def raise_for_status(self):
            pass

    class MockSession:
        def __init__(self):
            self.calls = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def get(self, url, headers=None, timeout=None):
            self.calls += 1
            if self.calls < 3:
                raise requests.exceptions.ConnectionError("boom")
            return MockResponse()

    session = MockSession()
    monkeypatch.setattr(start.requests, "Session", lambda: session)
    config.api_max_retries = 3
    config.api_retry_wait = 1
    waits = []
    monkeypatch.setattr(start.time, "sleep", lambda s: waits.append(s))
    assert start.fetch_futures_balance(config) == 123.45
    assert session.calls == 3
    assert waits == [1, 2]


def test_fetch_futures_balance_retries_fail(monkeypatch, config):
    class MockSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def get(self, url, headers=None, timeout=None):
            raise requests.exceptions.Timeout("timeout")

    monkeypatch.setattr(start.requests, "Session", lambda: MockSession())
    config.api_max_retries = 2
    config.api_retry_wait = 0
    monkeypatch.setattr(start.time, "sleep", lambda s: None)
    with pytest.raises(RuntimeError):
        start.fetch_futures_balance(config)


def test_fetch_futures_balance_invalid_json(monkeypatch, config):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise json.JSONDecodeError("msg", "doc", 0)

    class MockSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def get(self, url, headers=None, timeout=None):
            return MockResponse()

    monkeypatch.setattr(start.requests, "Session", lambda: MockSession())
    with pytest.raises(RuntimeError):
        start.fetch_futures_balance(config)


def test_write_and_read_balance(config, tmp_path):
    date = "2024-01-01"
    start.write_balance(config, date, 123.45)
    file_path = tmp_path / config.balance_folder / f"{date}.md"
    assert file_path.exists()
    assert "balance: 123.45" in file_path.read_text()
    # Read previous day's balance
    assert start.read_previous_balance(config, "2024-01-02") == 123.45


def test_read_previous_balance_creates_placeholder(config, tmp_path):
    balance = start.read_previous_balance(config, "2024-01-02")
    placeholder = tmp_path / config.balance_folder / "2024-01-01.md"
    assert balance == 0.0
    assert placeholder.exists()
    assert "balance: 0.00" in placeholder.read_text()


def test_mark_and_already_logged(config):
    config.today = "2024-01-01"
    assert not start.already_logged(config, "2024-01-01")
    start.mark_logged(config, "2024-01-01")
    assert start.already_logged(config, "2024-01-01")


def test_read_previous_balance_invalid_yaml(config, tmp_path, caplog):
    prev_date = "2024-01-01"
    file_path = tmp_path / config.balance_folder / f"{prev_date}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("---\n::not_yaml")
    with caplog.at_level(logging.WARNING):
        balance = start.read_previous_balance(config, "2024-01-02")
    assert balance == 0.0
    assert "Failed to parse balance file" in caplog.text


def test_already_logged_invalid_json(config, tmp_path, caplog):
    cache_file = tmp_path / "cache.json"
    cache_file.write_text("not-json")
    config.cache_file = str(cache_file)
    config.today = "2024-01-01"
    with caplog.at_level(logging.WARNING):
        assert not start.already_logged(config, "2024-01-01")
    assert "Failed to read cache file" in caplog.text

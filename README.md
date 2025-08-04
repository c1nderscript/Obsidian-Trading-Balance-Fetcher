# 🧾 Obsidian Trading Balance Fetcher

[![License: MIT](https://img.shields.io/github/license/c1nderscript/Obsidian-Trading-Balance-Fetcher)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![KuCoin API](https://img.shields.io/badge/api-kucoin-futures-blue)
![Obsidian](https://img.shields.io/badge/obsidian-integration-purple)
[![Last Commit](https://img.shields.io/github/last-commit/c1nderscript/Obsidian-Trading-Balance-Fetcher)](https://github.com/c1nderscript/Obsidian-Trading-Balance-Fetcher/commits/main)

Fetch your **KuCoin Futures account balance** and log it daily into a Markdown file for use with [Obsidian](https://obsidian.md/).

---

## 🚀 Features

- Fetches total account equity from KuCoin Futures
- Logs daily balance to `Trading/Balances/KuCoin/YYYY-MM-DD.md`
- Dataview-compatible YAML frontmatter
- Prevents duplicate logs via `~/.kucoin_balance_log.json`
- Computes daily PnL delta
- Supports manual backfilling via `--date YYYY-MM-DD`

---

## 📦 Setup

1. Clone the repository and enter it:
   ```bash
   git clone https://github.com/c1nderscript/Obsidian-Trading-Balance-Fetcher.git
   cd Obsidian-Trading-Balance-Fetcher
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r balancefetcher/requirements.txt
   ```
4. Create a `.env` file with your credentials:
   ```
   KUCOIN_API_KEY=<your key>
   KUCOIN_API_SECRET=<your secret>
   KUCOIN_API_PASSPHRASE=<your passphrase>
   OBSIDIAN_VAULT_PATH=<path to your Obsidian vault>
   ```
   Optionally set `KUCOIN_BALANCE_CURRENCY` (default `USDT`).

---

## 📈 Usage

Log today's balance:

```bash
python balancefetcher/start.py
```

Backfill a past date:

```bash
python balancefetcher/start.py --date 2025-08-01
```

Markdown files are saved to your vault as:

```markdown
---
date: 2025-08-02
balance: 111.15
---
```

---

## 📊 Obsidian Integration

Dataview table showing the last seven days:

```dataview
table date, balance
from "Trading/Balances/KuCoin"
sort date desc
limit 7
```

---

## 🛡 Security

- `.env` is excluded via `.gitignore`
- Only logs `accountEquity`, not positions or credentials

---

## 📜 License

[MIT License](https://opensource.org/licenses/MIT)

---

## ✨ Author

Developed by [@c1nderscript](https://github.com/c1nderscript) to integrate with [STRIDE](https://github.com/c1nderscript/STRIDE), Obsidian, and KuCoin.

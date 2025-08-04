# 🧾 Obsidian Trading Balance Fetcher

[![License: MIT](https://img.shields.io/github/license/c1nderscript/Obsidian-Trading-Balance-Fetcher)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![KuCoin API](https://img.shields.io/badge/api-kucoin-futures-blue)
![Obsidian](https://img.shields.io/badge/obsidian-integration-purple)
[![Last Commit](https://img.shields.io/github/last-commit/c1nderscript/Obsidian-Trading-Balance-Fetcher)](https://github.com/c1nderscript/Obsidian-Trading-Balance-Fetcher/commits/main)

Fetches your **KuCoin Futures account balance** and logs it daily into a Markdown file for use with [Obsidian](https://obsidian.md/), enabling seamless integration with [Dataview](https://github.com/blacksmithgu/obsidian-dataview), [Obsidian Charts](https://github.com/ZaidNaweed/obsidian-charts), and journaling workflows.

---

## 🚀 Features

- ✅ Fetches total account equity from KuCoin Futures
- ✅ Logs daily balance to `Trading/Balances/KuCoin/YYYY-MM-DD.md`
- ✅ Dataview-compatible YAML frontmatter
- ✅ Prevents duplicate logs via `.json` cache
- ✅ Computes daily PnL delta
- ✅ Supports manual backfilling via `--date YYYY-MM-DD`
- ✅ Configurable request timeout via `KUCOIN_API_TIMEOUT` (default 10s)
- ✅ Retry logic configurable via `KUCOIN_API_MAX_RETRIES` and `KUCOIN_API_RETRY_WAIT`

---

## 📦 Installation

```bash
git clone https://github.com/c1nderscript/Obsidian-Trading-Balance-Fetcher.git
cd Obsidian-Trading-Balance-Fetcher
python3 -m venv .venv
source .venv/bin/activate
pip install -r balancefetcher/requirements.txt
cp .env.example .env
```

Update `.env` with your credentials. `BALANCE_FOLDER` should point to the
folder inside your Obsidian vault where balances are stored, e.g.
`BALANCE_FOLDER=Trading/Balances/KuCoin`

Log today’s balance:

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

## 📊 Obsidian Integration

### Dataview Table (last 7 days)

```dataview
table date, balance
from "Trading/Balances/KuCoin"
sort date desc
limit 7
```

### Line Chart (DataviewJS + Obsidian Charts)

```dataviewjs
const pages = dv.pages('"Trading/Balances/KuCoin"')
  .where(p => p.date && p.balance)
  .sort(p => p.date, 'asc');

const labels = pages.map(p => p.date.toString());
const data = pages.map(p => p.balance);

dv.paragraph([
  "```chart",
  "type: line",
  `labels: [${labels.map(l => `"${l}"`).join(", ")}]`,
  "series:",
  "  - title: Balance",
  `    data: [${data.join(", ")}]`,
  "```",
].join("\n"));
```

---

## 💡 Quick Tips

Add ![[Trading/Charts/BalanceChart]] to any Obsidian note to show your balance chart.

## 🧪 Testing

Run the test suite with:

```bash
pip install -r balancefetcher/requirements.txt
pytest
```

## 🛡 Security

- `.env` is excluded via `.gitignore`
- Only logs `accountEquity`, not positions or credentials

---

## 📜 License

[MIT License](https://opensource.org/licenses/MIT)

---

## ✨ Author

Developed by [@c1nderscript](https://github.com/c1nderscript) to integrate with [STRIDE](https://github.com/c1nderscript/STRIDE), Obsidian, and KuCoin.


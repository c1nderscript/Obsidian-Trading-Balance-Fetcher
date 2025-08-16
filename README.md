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
- ✅ Cache location configurable via `BALANCE_CACHE_FILE` or `--cache-file`
- ✅ Computes daily PnL delta
- ✅ Supports manual backfilling via `--date YYYY-MM-DD`
- ✅ Configurable request timeout via `KUCOIN_API_TIMEOUT` (default 10s)
- ✅ Retry logic configurable via `KUCOIN_API_MAX_RETRIES` and `KUCOIN_API_RETRY_WAIT`

---

## 📦 Installation

Install from PyPI:

```bash
pip install obsidian-trading-balance-fetcher
```

Or install from source:

```bash
git clone https://github.com/c1nderscript/Obsidian-Trading-Balance-Fetcher.git
cd Obsidian-Trading-Balance-Fetcher
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
cp .env.example .env  # sample file lives at repo root

# Install development dependencies if you plan to run tests
# (includes runtime requirements automatically)
pip install -r requirements-dev.txt
```

Update `.env` with your credentials. `BALANCE_FOLDER` should point to the
folder inside your Obsidian vault where balances are stored, e.g.
`BALANCE_FOLDER=Trading/Balances/KuCoin`. The `.env.example` file documents all
optional settings such as `KUCOIN_BALANCE_CURRENCY`.

Optionally override the cache location:

```env
BALANCE_CACHE_FILE=/path/to/cache.json
```

Log today’s balance:

```bash
python balancefetcher/start.py
```

Backfill a past date:

```bash
python balancefetcher/start.py --date 2025-08-01
```

Specify a custom cache file:

```bash
python balancefetcher/start.py --cache-file /tmp/cache.json
```

Markdown files are saved to your vault as:

```markdown
---
date: 2025-08-02
balance: 111.15
---
```

## 🐳 Docker

Build the image:

```bash
docker build -t balancefetcher .
```

Run with your `.env` and mounted vault (set `OBSIDIAN_VAULT_PATH=/vault` in the env file):

```bash
docker run --rm --env-file .env -v /path/to/vault:/vault balancefetcher
```

For unattended daily execution, see the sample `docker-compose.yml`.

```bash
docker compose up -d
```

## 🛠 Deployment

### Environment variables

Copy the sample env file and fill in your credentials:

```bash
sudo cp .env.example /opt/balancefetcher/.env
sudo chmod 600 /opt/balancefetcher/.env
```

The application automatically loads this file when run from `/opt/balancefetcher`.

### Cron

Run the fetcher daily at midnight:

```cron
0 0 * * * cd /opt/balancefetcher && /usr/bin/python3 balancefetcher/start.py >> /var/log/balancefetcher.log 2>&1
```

### systemd

`/etc/systemd/system/balancefetcher.service`:

```ini
[Unit]
Description=Obsidian Trading Balance Fetcher

[Service]
Type=oneshot
EnvironmentFile=/opt/balancefetcher/.env
WorkingDirectory=/opt/balancefetcher
ExecStart=/usr/bin/python3 balancefetcher/start.py
```

`/etc/systemd/system/balancefetcher.timer`:

```ini
[Unit]
Description=Run balancefetcher daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Enable the timer:

```bash
sudo systemctl enable --now balancefetcher.timer
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

Run linters and the test suite with:

```bash
pip install -r requirements-dev.txt
pre-commit run --all-files
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


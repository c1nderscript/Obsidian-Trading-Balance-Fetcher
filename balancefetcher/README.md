# Step-by-Step: Set Up a Virtual Environment

## 1. Navigate to your project folder

```bash
cd ~/Documents/balancefetcher
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
```

This will create a `.venv/` folder inside your project with an isolated Python environment.

## 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

You'll see your prompt change to something like:

```bash
(.venv) [cinder@archlinux balancefetcher]$
```

## 4. Install required dependencies

```bash
pip install -r requirements.lock
```

## 5. (Optional) Install development dependencies

```bash
pip install -r requirements-dev.txt
```

## 6. Run your script inside the venv

```bash
python start.py
```

Install Obsidian Charts and Dataview in Obsidian, enable JS queries, then use this:

```dataviewjs
const pages = dv.pages('"Trading/Balances/KuCoin"')
    .where(p => p.balance && p.date)
    .sort(p => p.date, 'asc');

const labels = pages.map(p => p.date.toString());
const data = pages.map(p => p.balance);

const chart = [
  "```chart",
  "type: line",
  `labels: [${labels.map(l => `"${l}"`).join(", ")}]`,
  "series:",
  "  - title: Balance",
  `    data: [${data.join(", ")}]`,
  "```",
].join("\n");

dv.paragraph(chart);
```


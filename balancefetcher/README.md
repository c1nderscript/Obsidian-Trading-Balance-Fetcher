✅ Step-by-Step: Set Up a Virtual Environment
📁 1. Navigate to your project folder
bash
Copy
Edit
cd ~/Documents/balancefetcher
🐍 2. Create a virtual environment
bash
Copy
Edit
python3 -m venv .venv
This will create a .venv/ folder inside your project with an isolated Python environment.

⚙️ 3. Activate the virtual environment
bash
Copy
Edit
source .venv/bin/activate
You'll see your prompt change to something like:

bash
Copy
Edit
(.venv) [cinder@archlinux balancefetcher]$
📦 4. Install required dependencies
bash
Copy
Edit
pip install python-dotenv requests
📜 5. Freeze the dependencies (optional but good practice)
bash
Copy
Edit
pip freeze > requirements.txt
Now you have a reproducible environment.

▶️ 6. Run your script inside the venv
bash
Copy
Edit
python start.py



Install Obsidian Charts and Dataview in Obsidian, enable JS queries, use this

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
  "```"
].join("\n");

dv.paragraph(chart);
```




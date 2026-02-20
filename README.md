# 🥙 Nikos Cafe — Business Intelligence Dashboard

> **Live app:** *(paste your Streamlit Cloud URL here after deployment)*

A unified business intelligence dashboard for Nikos Cafe — a university campus food operation running under an Aramark/Sodexo contract. Combines daily POS sales data with supplier invoices into a single command center for ownership and operations.

---

## 📊 Dashboard Overview

| Tab | What it shows |
|-----|--------------|
| 📊 **Overview** | KPI cards, daily break-even tracker, week-over-week growth, weekly summary table |
| 📈 **Sales & Peak Periods** | Daily trend, day-of-week performance, Aramark/Sodexo discount rate by day, 15-min time slot drill-down |
| 📦 **Inventory Spending** | Category breakdown, top 12 items, weekly trend by vendor (RD vs PFS), category drill-down |
| 💰 **Food Cost & Margins** | Weekly food cost %, contract economics view (FC% vs net AND vs gross), net profitability after fees |
| ⚠️ **Overstock & Waste** | Weekly spend vs average, purchasing consistency, perishables spoilage watch |
| 🔔 **Alerts & Recovery** | Protein cost alert with item-level price trend, slow day recovery suggestions (university-specific) |

---

## 🏛️ University Contract Context

Nikos Cafe operates under an **Aramark/Sodexo campus dining contract**. This is important for reading the numbers correctly:

- **Discounts** are contract-mandated (meal plans, faculty/staff IDs) — not promotional choices
- **Food cost % vs Net Sales** (~42%) = operational kitchen view
- **Food cost % vs Gross Sales** (~27%) = contract economics view (for reporting to Aramark)
- **University contract benchmark**: 35–42% FC vs net sales (not the independent restaurant benchmark of 28–34%)

---

## 📁 Data Sources

| File | Source | Location in repo |
|------|--------|-----------------|
| `combined_sales_data.xlsx` | Oracle Micros Symphony (POS) + GetApp (online orders) | `data/` |
| `COMBINED_Master_Analysis.xlsx` | Restaurant Depot + Performance Food Service invoices | `data/` |
| `image.jpg` | Nikos Cafe logo | `data/` |

**Sales file format:** One Excel sheet per day named `YYYY-MM-DD`, containing gross sales, discounts, net sales, payment breakdown, and 15-minute time slot data.

**Inventory file format:** Single sheet `ALL_DATA` with columns: `Invoice_Date`, `Standard_Item_Name`, `Qty`, `Unit_Price`, `Total_Price`, `Category/Class`, `Subcategory`, `Source`.

---

## ⚙️ Sidebar Settings

All settings are adjustable live — no code changes needed.

| Setting | Default | Description |
|---------|---------|-------------|
| Aramark/Sodexo Commission % | 20% | Contract commission rate on net sales |
| Credit Card Fee % | 3% | Applied to CC transactions only |
| Target Food Cost % | 38% | University contract benchmark: 35–42% |
| Daily Fixed Costs ($) | $800 | Used for break-even tracker |
| Protein Budget Alert % | 35% | Alert fires when protein spend exceeds this |
| Peak slots (Top %) | 10% | For 15-min time slot highlighting |
| Slow slots (Bottom %) | 20% | For 15-min time slot highlighting |

---

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/nikos-cafe-dashboard.git
cd nikos-cafe-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run nikos_unified_dashboard.py
```

Dashboard opens at `http://localhost:8501`

---

## 📅 Daily Data Update

After adding new data to your Excel files, run:

```bash
./update.sh
```

This copies the latest Excel files into `data/`, commits, and pushes to GitHub. Streamlit Cloud redeploys automatically in ~60 seconds.

---

## 🏗️ Project Structure

```
nikos-cafe-dashboard/
│
├── nikos_unified_dashboard.py   ← Main Streamlit app
├── requirements.txt              ← Python dependencies
├── README.md                     ← This file
├── .gitignore                    ← Files excluded from git
├── update.sh                     ← Daily data push script
│
├── .streamlit/
│   └── config.toml               ← Forces light theme on all machines
│
└── data/
    ├── combined_sales_data.xlsx  ← Daily sales (POS exports)
    ├── COMBINED_Master_Analysis.xlsx ← Supplier invoices
    └── image.jpg                 ← Nikos Cafe logo
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data processing |
| [OpenPyXL](https://openpyxl.readthedocs.io) | Excel file reading |
| [NumPy](https://numpy.org) | Numerical calculations |

---

## 👤 Operations Info

- **Location:** University campus, operating under Aramark/Sodexo contract
- **POS:** Oracle Micros Symphony + GetApp (online orders)
- **Suppliers:** Restaurant Depot + Performance Food Service
- **Week cycle:** Thursday – Wednesday

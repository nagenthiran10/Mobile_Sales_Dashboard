# 📱 Global Mobile Sales Insights Dashboard

> A premium, enterprise-style analytics dashboard built with **Streamlit** and **Plotly** — tracking global mobile phone sales across brands, countries, age groups, and price segments from 2022 to 2025.

🔗 **Live Demo:** [mobile-sales-dashboard.streamlit.app](https://mobile-sales-dashboard.streamlit.app/)

![Dashboard Preview](images\preview.png)

---

## 🖥️ Dashboard Overview

The dashboard presents a single-page, no-scroll analytics experience on desktop, with a fully responsive layout on mobile. It is themed in a **dark charcoal + burnt orange** palette for a professional enterprise look.

### KPI Strip (Top Row)
Five headline metrics update in real time as filters are applied:

| Metric | Description |
|---|---|
| 💰 Total Revenue | Sum of all revenue, formatted in B/L/K |
| 📦 Total Units Sold | Aggregate units across filtered data |
| 🏷️ Avg Selling Price | Mean selling price of filtered records |
| 📈 Revenue Growth | Month-over-Month % change in revenue |
| 🧾 Total Orders | Count of unique order IDs |

Each KPI also shows a **Year-over-Year comparison** (▲/▼ vs Last Year) in green or orange.

---

## 📊 Charts & Visualisations

### 📈 Sales Trend Over Time *(Line Chart)*
Monthly units sold plotted as a filled area line chart, showing the full sales trajectory from Jan 2022 to Dec 2025.

### 🏆 Top Brands by Revenue *(Horizontal Bar Chart)*
Top 15 brands ranked by total revenue, with formatted revenue labels displayed outside each bar.

### 🌳 Age Group Distribution *(Treemap)*
Units sold broken down by buyer age group (18–24, 25–34, 35–44, 45–54, 55+), sized and coloured by volume.

### 🏷️ Price Segment Distribution *(Donut Chart)*
Share of orders across four price tiers: Budget, Mid-Range, Premium, and Ultra-Premium.

### 🌍 Sales by Country *(Choropleth Map)*
World map shaded by units sold per country, using a natural earth projection with a dark ocean background.

---

## 🎛️ Filters & Controls

### Desktop (Sidebar)
The burnt-orange sidebar contains all controls:
- **Year** — pill-style radio buttons: All / 2022 / 2023 / 2024 / 2025
- **Brand** — dropdown to filter by phone brand
- **Price** — dropdown to filter by price segment
- **Country** — dropdown to filter by country
- **Quick Insights** — auto-updated cards showing Top Brand, Top Country, and Top Model for the current selection

### Mobile (Inline Expander)
On mobile, the sidebar is hidden and replaced with a collapsible **"Filters & Quick Insights"** expander at the top of the page, keeping the full screen available for charts.

---

## 📱 Mobile Responsiveness

The dashboard uses **JavaScript-based mobile detection** (`window.innerWidth <= 768`) to inject a `?mobile=1` query parameter. Python reads this via `st.query_params` and renders a completely different layout:

| Feature | Desktop | Mobile |
|---|---|---|
| Filters | Fixed sidebar (burnt orange) | Collapsible inline expander |
| Main charts | 70/30 column split | Tabbed (Sales Trend / Top Brands) |
| Bottom charts | 3 columns side by side | Tabbed (Age Groups / Price / Map) |
| KPI strip | 5 cards in a row | 2×2 grid, 5th card full width |
| Page scroll | Locked (`overflow: hidden`) | Enabled (`overflow: auto`) |
| Chart height | 330px / 300px | 240px / 250px |

---

## 🗂️ Project Structure

```
├── app.py                      # Main Streamlit application
├── data/
│   └── mobile_sales_dataset.csv   # Source dataset
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ⚙️ Dataset Columns Used

| Column | Description |
|---|---|
| `brand` | Phone manufacturer (Apple, Samsung, etc.) |
| `model` | Specific phone model |
| `selling_price` | Unit selling price |
| `units_sold` | Number of units sold per record |
| `revenue` | Total revenue for the record |
| `order_id` | Unique order identifier |
| `country` | Country of sale |
| `buyer_age_group` | Age bracket of the buyer |
| `inward_date` | Date of the transaction |
| `year` | Year extracted from inward_date |

The app derives two additional columns at load time:
- `price_range` — quartile-based label (Budget / Mid-Range / Premium / Ultra-Premium)
- `month_year` — period string (e.g. `2023-07`) for the line chart

---

## 🚀 Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/your-username/Mobile_sales_dashboard.git
cd Mobile_sales_dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Place the dataset**

Put `mobile_sales_dataset.csv` inside a `data/` folder:
```
data/mobile_sales_dataset.csv
```

**4. Run the app**
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 Requirements

```
streamlit
pandas
plotly
numpy
```

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Line, treemap, pie, choropleth charts |
| [Plotly Graph Objects](https://plotly.com/python/graph-objects/) | Custom horizontal bar chart |
| [Pandas](https://pandas.pydata.org) | Data loading, filtering, aggregation |
| [NumPy](https://numpy.org) | Numerical support |
| Custom CSS + JS | Dark theme, mobile detection, KPI cards |

---

## ✨ Design Highlights

- **Zero-scroll desktop layout** — entire dashboard fits within one viewport using `height: 100vh` and `overflow: hidden`
- **Burnt orange (`#F26419`) accent** — consistent across sidebar, KPI borders, chart colours, and mobile header
- **YoY delta calculations** — each KPI automatically compares current year vs the previous year using the same active filters
- **Smart number formatting** — values display as B (billions), L (lakhs), or K (thousands) depending on magnitude
- **Collapsed borders** — chart panels share borders via negative margins for a tight grid feel
- **No modebar clutter** — Plotly modebar is hidden by default and only appears on hover (desktop)

---

## 📸 Preview

| Desktop | Mobile |
|-----------------------------------|--------------------------------|
| Full sidebar + 70/30 split layout | Tabbed charts + inline filters |

---

## 🙌 Author

Built by **Nagenthiran** · [GitHub](https://github.com/nagenthiran10)

---

> ⭐ If you found this useful, consider starring the repository!
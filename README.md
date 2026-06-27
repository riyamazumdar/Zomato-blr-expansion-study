# Zomato-blr-expansion-study
SQL, Python, Tableau, Power BI | Analyzed 51,000+ Zomato Bangalore Restaurants to identify opportunities for expansion, cuisine rich areas, and location level profitability signals. The project basically answers, where should zomato expand next?

## DATASET
the full dataset(548MB) is available on Kaggle:- https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants

---

## Phase 1 — Data Cleaning 

**Notebook:** `notebooks/01_data_cleaning.ipynb`

**What was done:**
- Loaded raw dataset — 51,717 rows, 17 columns
- Cleaned `rate` column — removed `/5`, `NEW`, `-` values
- Retained 10,031 unrated restaurants as a business insight 
  rather than dropping them
- Cleaned `cost_for_two` — removed commas, filled 346 nulls 
  with median (₹300)
- Converted `online_order` and `book_table` from Yes/No to 1/0
- Filled `rest_type`, `cuisines`, `primary_cuisine` nulls 
  with `Unknown`
- Added derived columns — `primary_cuisine`, `cuisine_count`
- Dropped irrelevant columns — `url`, `phone`, `reviews_list`, 
  `menu_item`
- Final clean dataset — **51,696 rows, 13 columns**

**Insights from cleaning:**
- ~20% of restaurants have no rating — significant engagement gap on the platform
- Cost ranges from ₹40 to ₹6,000 — extreme diversity from street food to fine dining
- 28,057 restaurants have no dish data — opportunity for Zomato to improve menu coverage

## Phase 2 — SQL Business Analysis ✅

**Notebooks:** `notebooks/02_load_to_sqlite.ipynb` · `notebooks/03_sql_analysis.ipynb`

**10 business questions answered using advanced SQL:**

| Query | Business Question | Key Finding |
|---|---|---|
| Q1 | Which areas are most profitable? | Koramangala & Indiranagar dominate |
| Q2 | Which cuisines dominate? | North Indian leads, Cafe culture rising |
| Q3 | Online vs offline performance? | Online restaurants rate higher |
| Q4 | Which restaurant types rate best? | Pubs & microbreweries lead |
| Q5 | Top restaurants per area? | AB's dominates across neighbourhoods |
| Q6 | Where to expand next? | Church Street, Lavelle Road, Koramangala 5th Block |
| Q7 | Do pricier areas rate better? | Premium areas show stronger ratings |
| Q8 | Does table booking matter? | Booking-enabled restaurants rate higher |
| Q9 | Top cuisine per neighbourhood? | Koramangala & Indiranagar are cuisine hotspots |
| Q10 | Where are users most engaged? | Church Street & Lavelle Road lead engagement |

**SQL techniques demonstrated:**
- Window functions — `ROW_NUMBER()`, `RANK()`, `NTILE()`
- CTEs (Common Table Expressions)
- `CASE WHEN` statements
- Subqueries
- `NULLIF`, `CAST`, `HAVING`
- Business logic scoring

**Headline finding:**
> Koramangala 5th Block, Indiranagar, Church Street, and Lavelle Road 
> consistently emerge as Bangalore's highest priority zones across 
> profitability, expansion opportunity, cuisine dominance, and user 
> engagement metrics.

---


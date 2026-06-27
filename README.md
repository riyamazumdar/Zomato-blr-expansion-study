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
## Phase 3 — Python EDA & ML Models ✅

**Notebooks:** `04_eda_and_visuals.ipynb` · `05_ml_success_score.ipynb` · 
`06_price_elasticity.ipynb`

### EDA — 10 Business Charts
- Top 15 locations by average rating
- Top 10 cuisines by customer engagement
- Online vs offline rating comparison
- Restaurant type performance
- Cost distribution by restaurant type
- Rating distribution across Bangalore
- Top 10 locations by engagement
- Cost vs rating scatterplot
- Expansion opportunity map
- Table booking vs no booking comparison

### ML Success Score Model
- **Algorithm:** Random Forest Classifier (100 trees)
- **Accuracy:** 91.4% | **Precision:** 93.8% | **Recall:** 75.8%
- **Top predictor:** Votes (customer engagement) dominates all other features
- **Key finding:** A well-positioned restaurant is 15x more likely to 
  succeed than a poorly positioned one
- **Location insight:** Lavelle Road has Bangalore's highest success rate
- **Cuisine insight:** Modern Indian has highest success rate despite 
  lower volume — significant market gap

### Price Elasticity Analysis
- Ratings increase consistently with price across all buckets
- Biggest quality jump occurs at ₹1000+ (avg rating 4.13)
- **Biryani** shows highest price elasticity — premium pricing works
- ₹200-400 is most crowded segment — new entrants should go budget 
  or premium to differentiate

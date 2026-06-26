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


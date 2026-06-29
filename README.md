# Where Should Zomato Expand Next? — A Bangalore Market Study

SQL · Python · Tableau · Power BI · Streamlit | Analysed 51,696 Zomato 
Bangalore restaurants to identify high-opportunity expansion zones, cuisine 
demand gaps, and location-level profitability signals.

---

## Project Status
- [x] Phase 1 — Data Cleaning
- [x] Phase 2 — SQL Business Analysis
- [x] Phase 3 — Python EDA and ML Models
- [x] Phase 4 — Power BI Dashboard
- [x] Phase 5 — Streamlit App

---

## The Business Question

Bangalore has 51,000 plus restaurants on Zomato but which neighbourhoods 
are underserved? Which cuisines have unmet demand? Where should Zomato 
focus next to maximise growth?

This project answers those questions using real data, advanced SQL 
analysis, machine learning models, and interactive dashboards — 
structured as a consulting-style market intelligence report.

---

## Live App

The full interactive dashboard is built in Streamlit with 5 analytical tabs:

- Location Analysis
- Cuisine Analysis
- Expansion Opportunity
- ML Insights
- Deep Dive Analysis

To run locally:
```bash
streamlit run streamlit_app/app.py
```

---

## Dataset

Source: [Zomato Bangalore Restaurants — Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)

The full dataset (548MB) is too large for GitHub. Download zomato.csv 
and place it in the data folder before running any notebooks.

A 1,000 row sample (zomato_sample.csv) is included for quick exploration.

| Property | Value |
|---|---|
| Total restaurants | 51,696 |
| Columns after cleaning | 13 |
| Location coverage | All major Bangalore neighbourhoods |
| Cost range | Rs 40 to Rs 6,000 for two people |
| Unrated restaurants | 10,031 (20%) |

---

## Tools and Technologies

| Layer | Tools |
|---|---|
| Data Cleaning | Python, Pandas, NumPy |
| Business SQL Analysis | SQLite, Advanced SQL |
| EDA and Visualisation | Matplotlib, Seaborn |
| ML Modelling | Scikit-learn, SciPy |
| Dashboard | Power BI |
| Live App | Streamlit |
| Version Control | Git, GitHub |

---

## Project Structure
data/

zomato_sample.csv

notebooks/

01_data_cleaning.ipynb

02_load_to_sqlite.ipynb

03_sql_analysis.ipynb

04_eda_and_visuals.ipynb

05_ml_success_score.ipynb

06_price_elasticity.ipynb

streamlit_app/

app.py

dashboards/

zomato_powerbi_dashboard.png

sql_queries/

report/

requirements.txt

README.md

---

## Phase 1 — Data Cleaning

Notebook: 01_data_cleaning.ipynb

- Loaded raw dataset — 51,717 rows, 17 columns
- Cleaned rate column — removed /5, NEW, and dash values
- Retained 10,031 unrated restaurants as a business insight rather 
  than dropping them
- Cleaned cost_for_two — removed commas, filled 346 nulls with 
  median (Rs 300)
- Converted online_order and book_table from Yes/No to 1/0
- Filled rest_type, cuisines, primary_cuisine nulls with Unknown
- Added derived columns — primary_cuisine, cuisine_count
- Dropped irrelevant columns — url, phone, reviews_list, menu_item
- Final clean dataset — 51,696 rows, 13 columns

Key insights from cleaning:

- 20% of restaurants have no rating — significant engagement gap 
  on the platform
- Cost ranges from Rs 40 to Rs 6,000 — extreme diversity from 
  street food to fine dining
- 28,057 restaurants have no dish data — opportunity for Zomato 
  to improve menu coverage

---

## Phase 2 — SQL Business Analysis

Notebooks: 02_load_to_sqlite.ipynb and 03_sql_analysis.ipynb

10 business questions answered using advanced SQL:

| Query | Business Question | Key Finding |
|---|---|---|
| Q1 | Which areas are most profitable? | Koramangala and Indiranagar dominate |
| Q2 | Which cuisines dominate? | North Indian leads, Cafe culture rising |
| Q3 | Online vs offline performance? | Online restaurants rate higher |
| Q4 | Which restaurant types rate best? | Pubs and microbreweries lead |
| Q5 | Top restaurants per area? | ABs dominates across neighbourhoods |
| Q6 | Where to expand next? | Church Street, Lavelle Road, Koramangala 5th Block |
| Q7 | Do pricier areas rate better? | Premium areas show stronger ratings |
| Q8 | Does table booking matter? | Booking-enabled restaurants rate higher |
| Q9 | Top cuisine per neighbourhood? | Koramangala and Indiranagar are cuisine hotspots |
| Q10 | Where are users most engaged? | Church Street and Lavelle Road lead engagement |

SQL techniques demonstrated:

- Window functions — ROW_NUMBER, RANK, NTILE
- CTEs (Common Table Expressions)
- CASE WHEN statements
- Subqueries
- NULLIF, CAST, HAVING
- Business logic scoring

Headline finding:

Koramangala 5th Block, Indiranagar, Church Street, and Lavelle Road 
consistently emerge as Bangalore's highest priority zones across 
profitability, expansion opportunity, cuisine dominance, and user 
engagement metrics.

---

## Phase 3 — Python EDA and ML Models

Notebooks: 04_eda_and_visuals.ipynb, 05_ml_success_score.ipynb, 
06_price_elasticity.ipynb

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

- Algorithm: Random Forest Classifier (100 trees)
- Accuracy: 91.4%
- Precision: 93.8%
- Recall: 75.8%
- Top predictor: Votes (customer engagement) dominates all features
- A well-positioned restaurant is 15x more likely to succeed than 
  a poorly positioned one
- Lavelle Road has Bangalore's highest restaurant success rate
- Modern Indian has highest success rate despite lower volume — 
  significant market gap

### Price Elasticity Analysis

- Ratings increase consistently with price across all buckets
- Biggest quality jump occurs at Rs 1000 plus (avg rating 4.13)
- Biryani shows highest price elasticity — premium pricing works
- Rs 200-400 is most crowded segment — new entrants should go 
  budget or premium to differentiate

---

## Phase 4 — Power BI Dashboard

An interactive dashboard built with Zomato's red brand theme featuring:

- 5 KPI cards — total restaurants, avg rating, avg cost, 
  online ordering percentage, rated restaurants percentage
- Top 15 locations by average rating
- Top 10 cuisines by total votes
- Online vs offline restaurant comparison
- Expansion opportunity scatter plot
- Price vs rating line chart
- 4 interactive slicers — online order, restaurant type, 
  price range, cuisine

Dashboard screenshot available in the dashboards folder.

---

## Phase 5 — Streamlit App

A fully interactive web application with 5 analytical tabs:

Tab 1 — Location Analysis
- Top 15 locations by average rating
- Top 10 locations by total votes
- Online vs offline comparison across rating, count, and cost

Tab 2 — Cuisine Analysis
- Top 10 cuisines by total votes
- Top 10 cuisines by average rating
- Price vs rating line chart across all price buckets

Tab 3 — Expansion Opportunity
- Demand vs supply scatter plot with expansion signals
- Expansion scorecard table — High Opportunity, Growing, Established

Tab 4 — ML Insights
- Model performance metrics
- Feature importance chart
- Success rate by location
- Key ML findings

Tab 5 — Deep Dive Analysis
- Restaurant type performance and cost distribution
- Book table vs no booking comparison
- Success rate by cuisine
- Price elasticity by cuisine
- Rating distribution histogram
- Cost vs rating scatterplot
- Top 20 performing restaurants table

---

## Key Findings

From SQL Analysis:

- Koramangala 5th Block is Bangalore's number one restaurant zone 
  by profitability, cuisine quality, and user engagement
- North Indian cuisine commands the highest customer engagement citywide
- Online ordering restaurants consistently outrate offline ones
- Pubs and microbreweries are Bangalore's highest rated restaurant format
- Church Street, Lavelle Road, and Koramangala 5th Block are prime 
  expansion zones

From ML Analysis:

- Votes is the single strongest predictor of restaurant success — 
  more important than location, cuisine, or price
- Lavelle Road has the highest restaurant success rate in Bangalore
- Modern Indian cuisine is underserved — high success rate but low volume
- A well-positioned restaurant with 500 plus votes is 15x more likely 
  to succeed than a newly opened one with no reviews

From Price Elasticity:

- Biryani has the highest price elasticity — customers pay more and 
  rate higher consistently
- The Rs 200-400 bracket is the most competitive with 14,307 restaurants
- Premium dining above Rs 1000 achieves significantly higher ratings (4.13)

Executive Recommendation:

Zomato should prioritise partner acquisition in Church Street, Lavelle 
Road, and Koramangala 5th Block — areas showing consistently high demand 
relative to current restaurant supply. New restaurant partners should be 
onboarded onto online ordering and table booking immediately, as both 
features correlate strongly with higher ratings and customer engagement.

---

## How to Run

1. Clone the repo

```bash
git clone https://github.com/yourusername/zomato-blr-expansion-study
cd zomato-blr-expansion-study
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Download full dataset

Place zomato.csv in the data folder from the Kaggle link above.

4. Run notebooks in order
01_data_cleaning.ipynb

02_load_to_sqlite.ipynb

03_sql_analysis.ipynb

04_eda_and_visuals.ipynb

05_ml_success_score.ipynb

06_price_elasticity.ipynb

5. Launch Streamlit app

```bash
streamlit run streamlit_app/app.py
```

---

## Author

Riya Majumdar

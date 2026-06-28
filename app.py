import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as scipy_stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Zomato Bangalore Intelligence",
    page_icon="zomato-logo-png.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #1a0000;
        border-right: 2px solid #e23744;
    }
    [data-testid="stMetric"] {
        background-color: #1a0000;
        border: 1px solid #e23744;
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] {
        color: #ff6b6b !important;
        font-size: 14px !important;
    }
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    h1 { color: #e23744 !important; }
    h2 { color: #ff6b6b !important; }
    h3 { color: #ffffff !important; }
    hr { border-color: #e23744 !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/zomato_clean.csv')
    return df

df = load_data()

with st.sidebar:
    st.markdown("### Filters")

    online_filter = st.radio(
        "Online Order",
        options=["All", "Yes", "No"],
        horizontal=True
    )

    rest_types = ["All"] + sorted(df['rest_type'].dropna().unique().tolist())
    rest_type_filter = st.selectbox("Restaurant Type", options=rest_types)

    min_cost = int(df['cost_for_two'].min())
    max_cost = int(df['cost_for_two'].max())
    price_range = st.slider(
        "Price Range",
        min_value=min_cost,
        max_value=max_cost,
        value=(min_cost, max_cost)
    )

    cuisines = ["All"] + sorted(df['primary_cuisine'].dropna().unique().tolist())
    cuisine_filter = st.selectbox("Primary Cuisine", options=cuisines)

    locations = ["All"] + sorted(df['location'].dropna().unique().tolist())
    location_filter = st.selectbox("Location", options=locations)

    df_filtered = df.copy()
    if online_filter != "All":
        df_filtered = df_filtered[
            df_filtered['online_order'] == (1 if online_filter == "Yes" else 0)
        ]
    if rest_type_filter != "All":
        df_filtered = df_filtered[df_filtered['rest_type'] == rest_type_filter]
    df_filtered = df_filtered[
        (df_filtered['cost_for_two'] >= price_range[0]) &
        (df_filtered['cost_for_two'] <= price_range[1])
    ]
    if cuisine_filter != "All":
        df_filtered = df_filtered[df_filtered['primary_cuisine'] == cuisine_filter]
    if location_filter != "All":
        df_filtered = df_filtered[df_filtered['location'] == location_filter]

    st.metric("Restaurants in View", f"{len(df_filtered):,}")
    st.caption("Built by Riya | KIIT 2026")

st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 42px; color: #e23744;'>
            WHERE SHOULD ZOMATO EXPAND NEXT
        </h1>
        <p style='color: #aaaaaa; font-size: 16px;'>
            Bangalore Restaurant Market Intelligence | 51,696 Restaurants Analysed
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Restaurants", f"{len(df_filtered):,}")
with col2:
    avg_rating = df_filtered['rate'].mean()
    st.metric("Avg Rating", f"{avg_rating:.2f}" if not np.isnan(avg_rating) else "N/A")
with col3:
    st.metric("Avg Cost for Two", f"Rs {df_filtered['cost_for_two'].mean():.0f}")
with col4:
    online_pct = df_filtered['online_order'].mean() * 100
    st.metric("Online Ordering", f"{online_pct:.1f}%")
with col5:
    rated_pct = df_filtered['rate'].notna().mean() * 100
    st.metric("Rated Restaurants", f"{rated_pct:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Location Analysis",
    "Cuisine Analysis",
    "Expansion Opportunity",
    "ML Insights",
    "Deep Dive Analysis"
])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 15 Locations by Avg Rating")
        top_locations = (df_filtered[df_filtered['rate'].notna()]
                         .groupby('location')
                         .agg(avg_rating=('rate', 'mean'),
                              count=('name', 'count'))
                         .query('count >= 10')
                         .sort_values('avg_rating', ascending=False)
                         .head(15)
                         .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        colors = ['#e23744' if i == 0 else '#ff6b6b'
                  for i in range(len(top_locations))]
        bars = ax.barh(top_locations['location'],
                       top_locations['avg_rating'],
                       color=colors)
        ax.set_xlabel('Average Rating', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for bar, val in zip(bars, top_locations['avg_rating']):
            ax.text(bar.get_width() + 0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'{val:.2f}', va='center',
                    color='white', fontsize=8)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Top 10 Locations by Total Votes")
        top_votes = (df_filtered.groupby('location')
                     .agg(total_votes=('votes', 'sum'),
                          count=('name', 'count'))
                     .query('count >= 10')
                     .sort_values('total_votes', ascending=False)
                     .head(10)
                     .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        ax.barh(top_votes['location'],
                top_votes['total_votes'],
                color='#ff6b6b')
        ax.set_xlabel('Total Votes', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Online vs Offline Performance")
    col1, col2, col3 = st.columns(3)

    online_stats = (df_filtered[df_filtered['rate'].notna()]
                    .groupby('online_order')
                    .agg(avg_rating=('rate', 'mean'),
                         count=('name', 'count'),
                         avg_cost=('cost_for_two', 'mean'))
                    .reset_index())
    online_stats['mode'] = online_stats['online_order'].map({1: 'Online', 0: 'Offline'})

    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(online_stats['mode'],
                      online_stats['avg_rating'],
                      color=['#e23744', '#ff6b6b'], width=0.4)
        for bar, val in zip(bars, online_stats['avg_rating']):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.01,
                    f'{val:.2f}', ha='center',
                    color='white', fontweight='bold')
        ax.set_ylabel('Avg Rating', color='white')
        ax.set_ylim(3.0, 4.5)
        ax.set_title('Avg Rating', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(online_stats['mode'],
                      online_stats['count'],
                      color=['#e23744', '#ff6b6b'], width=0.4)
        for bar, val in zip(bars, online_stats['count']):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 100,
                    f'{val:,}', ha='center',
                    color='white', fontweight='bold', fontsize=8)
        ax.set_ylabel('Count', color='white')
        ax.set_title('Restaurant Count', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col3:
        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(online_stats['mode'],
                      online_stats['avg_cost'],
                      color=['#e23744', '#ff6b6b'], width=0.4)
        for bar, val in zip(bars, online_stats['avg_cost']):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 5,
                    f'Rs {val:.0f}', ha='center',
                    color='white', fontweight='bold', fontsize=8)
        ax.set_ylabel('Avg Cost', color='white')
        ax.set_title('Avg Cost for Two', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 10 Cuisines by Total Votes")
        top_cuisines = (df_filtered[df_filtered['primary_cuisine'] != 'Unknown']
                        .groupby('primary_cuisine')
                        .agg(total_votes=('votes', 'sum'),
                             count=('name', 'count'),
                             avg_rating=('rate', 'mean'))
                        .query('count >= 10')
                        .sort_values('total_votes', ascending=False)
                        .head(10)
                        .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        ax.barh(top_cuisines['primary_cuisine'],
                top_cuisines['total_votes'],
                color='#e23744')
        ax.set_xlabel('Total Votes', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Top 10 Cuisines by Avg Rating")
        top_cuisine_rating = (df_filtered[
            (df_filtered['primary_cuisine'] != 'Unknown') &
            (df_filtered['rate'].notna())]
            .groupby('primary_cuisine')
            .agg(avg_rating=('rate', 'mean'),
                 count=('name', 'count'))
            .query('count >= 20')
            .sort_values('avg_rating', ascending=False)
            .head(10)
            .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        ax.barh(top_cuisine_rating['primary_cuisine'],
                top_cuisine_rating['avg_rating'],
                color='#ff6b6b')
        ax.set_xlabel('Average Rating', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Price vs Rating")
    df_price = df_filtered[df_filtered['rate'].notna() &
                           df_filtered['cost_for_two'].notna()].copy()
    df_price['price_bucket'] = pd.cut(
        df_price['cost_for_two'],
        bins=[0, 200, 400, 600, 800, 1000, 6000],
        labels=['0-200', '200-400', '400-600',
                '600-800', '800-1000', '1000+']
    )
    price_rating = (df_price.groupby('price_bucket', observed=True)
                    .agg(avg_rating=('rate', 'mean'),
                         count=('name', 'count'))
                    .reset_index())

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(price_rating['price_bucket'],
            price_rating['avg_rating'],
            marker='o', linewidth=2.5,
            color='#e23744', markersize=10)
    for i, row in price_rating.iterrows():
        ax.text(i, row['avg_rating'] + 0.02,
                f"{row['avg_rating']:.2f}",
                ha='center', color='white', fontweight='bold')
    ax.set_xlabel('Price Bucket (Rs)', color='white')
    ax.set_ylabel('Average Rating', color='white')
    ax.set_facecolor('#0d0d0d')
    fig.patch.set_facecolor('#0d0d0d')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#e23744')
    ax.spines['left'].set_color('#e23744')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

with tab3:
    st.markdown("### Expansion Opportunity Score")
    st.markdown("High demand combined with low supply indicates a prime expansion zone")

    location_stats = (df_filtered.groupby('location')
                      .agg(restaurant_count=('name', 'count'),
                           total_votes=('votes', 'sum'),
                           avg_rating=('rate', 'mean'),
                           avg_cost=('cost_for_two', 'mean'))
                      .reset_index())
    location_stats['demand_per_restaurant'] = (
        location_stats['total_votes'] /
        location_stats['restaurant_count']
    ).round(0)
    location_stats['expansion_signal'] = location_stats.apply(
        lambda x: 'High Opportunity' if x['demand_per_restaurant'] > 500
        and x['restaurant_count'] < 100
        else ('Growing' if x['demand_per_restaurant'] > 300
              and x['restaurant_count'] < 150
              else 'Established'),
        axis=1
    )

    top_opp = (location_stats
               .query('restaurant_count >= 10')
               .sort_values('demand_per_restaurant', ascending=False)
               .head(15))

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 7))
        colors = ['#e23744' if s == 'High Opportunity'
                  else '#ff6b6b' if s == 'Growing'
                  else '#888888'
                  for s in top_opp['expansion_signal']]
        ax.scatter(top_opp['restaurant_count'],
                   top_opp['total_votes'],
                   s=top_opp['demand_per_restaurant'] / 2,
                   c=colors, alpha=0.8)
        for _, row in top_opp.iterrows():
            ax.annotate(row['location'],
                        (row['restaurant_count'], row['total_votes']),
                        textcoords="offset points",
                        xytext=(5, 5), fontsize=8, color='white')
        ax.set_xlabel('Number of Restaurants (Supply)', color='white')
        ax.set_ylabel('Total Votes (Demand)', color='white')
        ax.set_title('Demand vs Supply by Location', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Expansion Scorecard")
        display_cols = ['location', 'restaurant_count',
                        'demand_per_restaurant', 'expansion_signal']
        st.dataframe(
            top_opp[display_cols].rename(columns={
                'location': 'Location',
                'restaurant_count': 'Restaurants',
                'demand_per_restaurant': 'Demand Score',
                'expansion_signal': 'Signal'
            }),
            use_container_width=True,
            height=400
        )

with tab4:
    st.markdown("### ML Model Performance")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "91.4%")
    with col2:
        st.metric("Precision", "93.8%")
    with col3:
        st.metric("Recall", "75.8%")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Feature Importance")
        features = ['Votes', 'Cost for Two', 'Location',
                    'Rest Type', 'Cuisine Count',
                    'Online Order', 'Book Table', 'Cuisine']
        importance = [0.42, 0.18, 0.15, 0.10, 0.07, 0.04, 0.03, 0.01]

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#e23744' if i == 0 else '#ff6b6b'
                  for i in range(len(features))]
        ax.barh(features, importance, color=colors)
        ax.set_xlabel('Importance Score', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Success Rate by Location")
        df_model = df_filtered[df_filtered['rate'].notna()].copy()
        df_model['is_successful'] = (df_model['rate'] >= 4.0).astype(int)

        loc_success = (df_model.groupby('location')
                       .agg(total=('is_successful', 'count'),
                            successful=('is_successful', 'sum'))
                       .query('total >= 20')
                       .assign(success_rate=lambda x:
                               round(x['successful'] / x['total'] * 100, 1))
                       .sort_values('success_rate', ascending=False)
                       .head(10)
                       .reset_index())

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(loc_success['location'],
                loc_success['success_rate'],
                color='#e23744')
        ax.set_xlabel('Success Rate (%)', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Key ML Findings")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.error("Top Predictor: Votes drive success more than location or price")
    with col2:
        st.error("15x More Likely: Well-positioned restaurants with 500 plus votes succeed significantly more")
    with col3:
        st.error("Top Location: Lavelle Road has Bangalore highest restaurant success rate")
    with col4:
        st.error("Hidden Gem: Modern Indian has highest success rate despite low volume")

with tab5:
    st.markdown("### Restaurant Type Performance")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Restaurant Types by Avg Rating")
        rest_type_stats = (df_filtered[df_filtered['rate'].notna()]
                           .query("rest_type != 'Unknown'")
                           .groupby('rest_type')
                           .agg(avg_rating=('rate', 'mean'),
                                count=('name', 'count'))
                           .query('count >= 30')
                           .sort_values('avg_rating', ascending=False)
                           .head(10)
                           .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        ax.barh(rest_type_stats['rest_type'],
                rest_type_stats['avg_rating'],
                color='#e23744')
        ax.set_xlabel('Average Rating', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Cost Distribution by Restaurant Type")
        top_types = df_filtered['rest_type'].value_counts().head(8).index
        df_type = df_filtered[df_filtered['rest_type'].isin(top_types)]

        fig, ax = plt.subplots(figsize=(9, 7))
        bp = ax.boxplot(
            [df_type[df_type['rest_type'] == t]['cost_for_two'].dropna()
             for t in top_types],
            labels=top_types,
            patch_artist=True,
            boxprops=dict(facecolor='#e23744', color='white'),
            medianprops=dict(color='white'),
            whiskerprops=dict(color='white'),
            capprops=dict(color='white'),
            flierprops=dict(color='white', markeredgecolor='white')
        )
        ax.set_ylabel('Cost for Two (Rs)', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        plt.xticks(rotation=45, ha='right', color='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Book Table Analysis")
    col1, col2 = st.columns(2)

    book_stats = (df_filtered[df_filtered['rate'].notna()]
                  .groupby('book_table')
                  .agg(avg_rating=('rate', 'mean'),
                       count=('name', 'count'),
                       avg_cost=('cost_for_two', 'mean'))
                  .reset_index())
    book_stats['booking'] = book_stats['book_table'].map(
        {1: 'Accepts Booking', 0: 'No Booking'}
    )

    with col1:
        st.markdown("#### Avg Rating by Booking Status")
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(book_stats['booking'],
                      book_stats['avg_rating'],
                      color=['#e23744', '#ff6b6b'],
                      width=0.4)
        for bar, val in zip(bars, book_stats['avg_rating']):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.01,
                    f'{val:.2f}', ha='center',
                    color='white', fontweight='bold')
        ax.set_ylabel('Average Rating', color='white')
        ax.set_ylim(3.0, 4.5)
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Avg Cost by Booking Status")
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(book_stats['booking'],
                      book_stats['avg_cost'],
                      color=['#e23744', '#ff6b6b'],
                      width=0.4)
        for bar, val in zip(bars, book_stats['avg_cost']):
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 5,
                    f'Rs {val:.0f}', ha='center',
                    color='white', fontweight='bold')
        ax.set_ylabel('Avg Cost for Two (Rs)', color='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Success Rate by Cuisine")
    df_success = df_filtered[df_filtered['rate'].notna()].copy()
    df_success['is_successful'] = (df_success['rate'] >= 4.0).astype(int)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Cuisines by Success Rate")
        cuisine_success = (df_success[df_success['primary_cuisine'] != 'Unknown']
                           .groupby('primary_cuisine')
                           .agg(total=('is_successful', 'count'),
                                successful=('is_successful', 'sum'))
                           .query('total >= 30')
                           .assign(success_rate=lambda x:
                                   round(x['successful'] / x['total'] * 100, 1))
                           .sort_values('success_rate', ascending=False)
                           .head(10)
                           .reset_index())

        fig, ax = plt.subplots(figsize=(9, 7))
        bars = ax.barh(cuisine_success['primary_cuisine'],
                       cuisine_success['success_rate'],
                       color='#e23744')
        for bar, val in zip(bars, cuisine_success['success_rate']):
            ax.text(bar.get_width() + 0.3,
                    bar.get_y() + bar.get_height()/2,
                    f'{val}%', va='center',
                    color='white', fontweight='bold', fontsize=9)
        ax.set_xlabel('Success Rate (%)', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Price Elasticity by Cuisine")
        top_cuisines_list = (df_filtered['primary_cuisine']
                             .value_counts()
                             .head(10)
                             .index.tolist())

        elasticity_results = []
        for cuisine in top_cuisines_list:
            data = df_filtered[
                (df_filtered['primary_cuisine'] == cuisine) &
                (df_filtered['rate'].notna()) &
                (df_filtered['cost_for_two'].notna())
            ].copy()
            if len(data) >= 30:
                slope, _, r_value, p_value, _ = scipy_stats.linregress(
                    data['cost_for_two'], data['rate']
                )
                elasticity_results.append({
                    'cuisine': cuisine,
                    'elasticity': round(slope * 100, 4),
                    'r_squared': round(r_value**2, 3),
                    'sample_size': len(data)
                })

        elasticity_df = pd.DataFrame(elasticity_results).sort_values(
            'elasticity', ascending=False
        )

        fig, ax = plt.subplots(figsize=(9, 7))
        colors = ['#e23744' if i == 0 else '#ff6b6b'
                  for i in range(len(elasticity_df))]
        bars = ax.barh(elasticity_df['cuisine'],
                       elasticity_df['elasticity'],
                       color=colors)
        for bar, val in zip(bars, elasticity_df['elasticity']):
            ax.text(bar.get_width() + 0.0001,
                    bar.get_y() + bar.get_height()/2,
                    f'{val:.4f}', va='center',
                    color='white', fontsize=8)
        ax.set_xlabel('Price Elasticity', color='white')
        ax.invert_yaxis()
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Rating Distribution and Cost vs Rating")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Rating Distribution across Bangalore")
        fig, ax = plt.subplots(figsize=(9, 6))
        df_filtered['rate'].dropna().plot(
            kind='hist', bins=30,
            color='#e23744', edgecolor='#0d0d0d', ax=ax
        )
        ax.axvline(df_filtered['rate'].mean(),
                   color='white', linestyle='--',
                   label=f'Mean: {df_filtered["rate"].mean():.2f}')
        ax.axvline(df_filtered['rate'].median(),
                   color='#ff6b6b', linestyle='--',
                   label=f'Median: {df_filtered["rate"].median():.2f}')
        ax.set_xlabel('Rating', color='white')
        ax.set_ylabel('Number of Restaurants', color='white')
        ax.legend(facecolor='#1a0000', labelcolor='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Cost vs Rating Scatterplot")
        df_scatter = df_filtered[
            df_filtered['rate'].notna() &
            df_filtered['cost_for_two'].notna()
        ].copy()

        fig, ax = plt.subplots(figsize=(9, 6))
        ax.scatter(df_scatter['cost_for_two'],
                   df_scatter['rate'],
                   alpha=0.3, color='#e23744', s=10)
        z = np.polyfit(df_scatter['cost_for_two'],
                       df_scatter['rate'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df_scatter['cost_for_two'].min(),
                             df_scatter['cost_for_two'].max(), 100)
        ax.plot(x_line, p(x_line), 'white',
                linestyle='--', linewidth=2, label='Trend')
        ax.set_xlabel('Cost for Two (Rs)', color='white')
        ax.set_ylabel('Rating', color='white')
        ax.legend(facecolor='#1a0000', labelcolor='white')
        ax.set_facecolor('#0d0d0d')
        fig.patch.set_facecolor('#0d0d0d')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('#e23744')
        ax.spines['left'].set_color('#e23744')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.markdown("### Top 20 Performing Restaurants")
    top_restaurants = (df_filtered[df_filtered['rate'].notna()]
                       .query('votes >= 100')
                       .sort_values(['rate', 'votes'], ascending=False)
                       .head(20)[['name', 'location', 'rest_type',
                                  'primary_cuisine', 'rate',
                                  'votes', 'cost_for_two',
                                  'online_order', 'book_table']]
                       .rename(columns={
                           'name': 'Restaurant',
                           'location': 'Location',
                           'rest_type': 'Type',
                           'primary_cuisine': 'Cuisine',
                           'rate': 'Rating',
                           'votes': 'Votes',
                           'cost_for_two': 'Cost for Two',
                           'online_order': 'Online Order',
                           'book_table': 'Book Table'
                       })
                       .reset_index(drop=True))

    top_restaurants['Online Order'] = top_restaurants['Online Order'].map(
        {1: 'Yes', 0: 'No'}
    )
    top_restaurants['Book Table'] = top_restaurants['Book Table'].map(
        {1: 'Yes', 0: 'No'}
    )

    st.dataframe(top_restaurants, use_container_width=True, height=400)

st.markdown("""
    <div style='text-align: center; color: #888888; padding: 10px;'>
        Built by Riya | CS Engineering KIIT 2026 |
        Zomato Bangalore Market Intelligence Study
    </div>
""", unsafe_allow_html=True)
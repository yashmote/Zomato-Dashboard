import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("zomato_cleaned.csv.gz")

st.title("📊 Restaurant Success Analysis in Bangalore")

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Filters")

locations = ["All"] + sorted(df['location'].dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

cuisines = ["All"] + sorted(df['cuisines'].dropna().unique())
selected_cuisine = st.sidebar.selectbox("Select Cuisine", cuisines)

online_option = st.sidebar.selectbox("Online Order", ["All", "Yes", "No"])

filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_location]

if selected_cuisine != "All":
    filtered_df = filtered_df[filtered_df['cuisines'].str.contains(selected_cuisine, na=False)]

if online_option != "All":
    value = 1 if online_option == "Yes" else 0
    filtered_df = filtered_df[filtered_df['online_order'] == value]

st.caption(f"Showing: {selected_location} | {selected_cuisine} | Online: {online_option}")

# ----------------------------
# Key Metrics
# ----------------------------

st.subheader("📊 Key Metrics")

avg_rating = filtered_df['rate'].mean()
avg_cost = filtered_df['approx_cost(for two people)'].mean()
total = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Average Rating", round(avg_rating, 2) if pd.notna(avg_rating) else "N/A")
col2.metric("Average Cost for Two", int(avg_cost) if pd.notna(avg_cost) else "N/A")
col3.metric("Total Restaurants", total)

# ----------------------------
# Competition Level
# ----------------------------

if filtered_df.shape[0] > 0:
    count = filtered_df.shape[0]

    if count < 50:
        comp_level = "Low"
    elif count < 150:
        comp_level = "Moderate"
    else:
        comp_level = "High"

    st.write(f"• Competition level in this segment: **{comp_level} ({count} restaurants)**")

# ----------------------------
# Visualizations
# ----------------------------

st.subheader("Rating Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df['rate'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

st.subheader("Cost vs Rating")
fig, ax = plt.subplots()
sns.scatterplot(
    x=filtered_df['approx_cost(for two people)'],
    y=filtered_df['rate'],
    ax=ax
)
st.pyplot(fig)

st.subheader("Online Ordering Impact")
fig, ax = plt.subplots()
sns.boxplot(x='online_order', y='rate', data=filtered_df, ax=ax)
st.pyplot(fig)

# ----------------------------
# Insights
# ----------------------------

st.subheader("📊 Key Insights")

if filtered_df.shape[0] > 0:

    online_rating = filtered_df.groupby('online_order')['rate'].mean()

    st.write(f"• Average rating: **{round(avg_rating,2)}**")

    if avg_cost < 400:
        st.write(f"• Budget segment performs at ~{round(avg_rating,2)} rating")
    elif avg_cost < 800:
        st.write(f"• Mid-range (₹400–₹800) shows stable performance (~{round(avg_rating,2)})")
    else:
        st.write(f"• Premium pricing does not outperform (~{round(avg_rating,2)})")

    if 1 in online_rating.index and 0 in online_rating.index:
        diff = online_rating[1] - online_rating[0]
        sign = "+" if diff > 0 else ""
        st.write(f"• Online ordering impact: **{sign}{round(diff,2)} rating difference**")

# ----------------------------
# Model Explanation
# ----------------------------

st.markdown("""
### 📊 Opportunity Score Logic

We define opportunity using:

- **Demand → Rating (higher is better)**
- **Competition → Restaurant count (lower is better)**

We normalize both and compute:

**Opportunity = High Demand + Low Competition**
""")

# ----------------------------
# Global Location Opportunity
# ----------------------------

st.markdown("### 📍 Best Locations to Open a Restaurant (Global Analysis)")
st.caption("Ignores location filter to identify new market opportunities.")

opportunity_df = df.copy()

if selected_cuisine != "All":
    opportunity_df = opportunity_df[
        opportunity_df['cuisines'].str.contains(selected_cuisine, na=False)
    ]

if online_option != "All":
    value = 1 if online_option == "Yes" else 0
    opportunity_df = opportunity_df[
        opportunity_df['online_order'] == value
    ]

location_analysis = opportunity_df.groupby('location').agg({
    'rate': 'mean',
    'name': 'count'
}).rename(columns={'name': 'restaurant_count'})

location_analysis['rating_norm'] = (
    (location_analysis['rate'] - location_analysis['rate'].min()) /
    (location_analysis['rate'].max() - location_analysis['rate'].min() + 1e-6)
)

location_analysis['competition_norm'] = (
    (location_analysis['restaurant_count'] - location_analysis['restaurant_count'].min()) /
    (location_analysis['restaurant_count'].max() - location_analysis['restaurant_count'].min() + 1e-6)
)

location_analysis['opportunity_score'] = (
    0.5 * location_analysis['rating_norm'] +
    0.5 * (1 - location_analysis['competition_norm'])
)

top_opportunities = location_analysis.sort_values(by='opportunity_score', ascending=False).head(5)

st.write(top_opportunities[['rate', 'restaurant_count', 'opportunity_score']])

# ----------------------------
# Cuisine Opportunities (TABLE)
# ----------------------------

st.markdown("### 🍽️ Underserved Cuisine Opportunities (Filtered View)")
st.caption("Based on selected filters — shows local cuisine gaps.")

if filtered_df.shape[0] > 0:

    cuisine_df = filtered_df.copy()
    cuisine_df = cuisine_df.assign(
        cuisine=cuisine_df['cuisines'].str.split(', ')
    ).explode('cuisine')

    cuisine_analysis = cuisine_df.groupby('cuisine').agg({
        'rate': 'mean',
        'name': 'count'
    }).rename(columns={'name': 'restaurant_count'})

    cuisine_analysis['rating_norm'] = (
        (cuisine_analysis['rate'] - cuisine_analysis['rate'].min()) /
        (cuisine_analysis['rate'].max() - cuisine_analysis['rate'].min() + 1e-6)
    )

    cuisine_analysis['competition_norm'] = (
        (cuisine_analysis['restaurant_count'] - cuisine_analysis['restaurant_count'].min()) /
        (cuisine_analysis['restaurant_count'].max() - cuisine_analysis['restaurant_count'].min() + 1e-6)
    )

    cuisine_analysis['opportunity_score'] = (
        0.6 * cuisine_analysis['rating_norm'] +
        0.4 * (1 - cuisine_analysis['competition_norm'])
    )

    top_cuisines = cuisine_analysis.sort_values(
        by='opportunity_score', ascending=False
    ).head(5)

    st.write(top_cuisines[['rate', 'restaurant_count', 'opportunity_score']])

# ----------------------------
# 🌍 GLOBAL RECOMMENDATION
# ----------------------------

st.subheader("🌍 Global Strategy Recommendation")

if not top_opportunities.empty:

    best_location = top_opportunities.index[0]
    best_loc_df = df[df['location'] == best_location]

    # Cuisine for best location
    cuisine_df = best_loc_df.copy()
    cuisine_df = cuisine_df.assign(
        cuisine=cuisine_df['cuisines'].str.split(', ')
    ).explode('cuisine')

    cuisine_analysis = cuisine_df.groupby('cuisine').agg({
        'rate': 'mean',
        'name': 'count'
    }).rename(columns={'name': 'restaurant_count'})

    cuisine_analysis['rating_norm'] = (
        (cuisine_analysis['rate'] - cuisine_analysis['rate'].min()) /
        (cuisine_analysis['rate'].max() - cuisine_analysis['rate'].min() + 1e-6)
    )

    cuisine_analysis['competition_norm'] = (
        (cuisine_analysis['restaurant_count'] - cuisine_analysis['restaurant_count'].min()) /
        (cuisine_analysis['restaurant_count'].max() - cuisine_analysis['restaurant_count'].min() + 1e-6)
    )

    cuisine_analysis['opportunity_score'] = (
        0.6 * cuisine_analysis['rating_norm'] +
        0.4 * (1 - cuisine_analysis['competition_norm'])
    )

    best_cuisine = cuisine_analysis.sort_values(
        by='opportunity_score', ascending=False
    ).index[0]

    best_avg_cost = best_loc_df['approx_cost(for two people)'].mean()

    if best_avg_cost < 400:
        price_range = "₹300–₹400 (Budget)"
    elif best_avg_cost < 800:
        price_range = "₹400–₹800 (Mid-range)"
    else:
        price_range = "₹800+ (Premium)"

    st.success(f"""
**Best Overall Market Entry**

• **Location:** {best_location}  
• **Cuisine:** {best_cuisine}  
• **Pricing:** {price_range}  

👉 Optimized for demand and low competition across Bangalore.
""")

# ----------------------------
# 📍 LOCAL RECOMMENDATION
# ----------------------------

st.subheader("📍 Local Strategy Recommendation")

if filtered_df.shape[0] > 0:

    local_df = filtered_df.copy()

    # Cuisine (local)
    cuisine_df = local_df.assign(
        cuisine=local_df['cuisines'].str.split(', ')
    ).explode('cuisine')

    cuisine_analysis = cuisine_df.groupby('cuisine').agg({
        'rate': 'mean',
        'name': 'count'
    }).rename(columns={'name': 'restaurant_count'})

    cuisine_analysis['rating_norm'] = (
        (cuisine_analysis['rate'] - cuisine_analysis['rate'].min()) /
        (cuisine_analysis['rate'].max() - cuisine_analysis['rate'].min() + 1e-6)
    )

    cuisine_analysis['competition_norm'] = (
        (cuisine_analysis['restaurant_count'] - cuisine_analysis['restaurant_count'].min()) /
        (cuisine_analysis['restaurant_count'].max() - cuisine_analysis['restaurant_count'].min() + 1e-6)
    )

    cuisine_analysis['opportunity_score'] = (
        0.6 * cuisine_analysis['rating_norm'] +
        0.4 * (1 - cuisine_analysis['competition_norm'])
    )

    local_best_cuisine = cuisine_analysis.sort_values(
        by='opportunity_score', ascending=False
    ).index[0]

    # Pricing (local)
    local_avg_cost = local_df['approx_cost(for two people)'].mean()

    if local_avg_cost < 400:
        local_price = "₹300–₹400 (Budget)"
    elif local_avg_cost < 800:
        local_price = "₹400–₹800 (Mid-range)"
    else:
        local_price = "₹800+ (Premium)"

    st.info(f"""
**Strategy for Current Selection**

• **Location:** {selected_location if selected_location != "All" else "Selected Area"}  
• **Cuisine:** {local_best_cuisine}  
• **Pricing:** {local_price}  

👉 Tailored to current filters and local competition.
""")
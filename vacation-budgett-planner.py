import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Theme Toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
            body { background-color: #1e1e1e; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Currency Conversion (Basic Static Rates for Now)
currency_rates = {"USD": 1, "EUR": 0.91, "GBP": 0.78, "PKR": 278}
currency = st.sidebar.selectbox("💱 Select Currency", list(currency_rates.keys()), index=0)

# User Inputs
destination = st.sidebar.text_input("🌍 Destination", "Paris")
budget_usd = st.sidebar.slider("💰 Total Budget ($)", 500, 10000, 2500)
budget = budget_usd * currency_rates[currency]  # Convert to selected currency
travel_style = st.sidebar.selectbox("🏨 Travel Style", ["Budget", "Mid-range", "Luxury"])
years_ahead = st.sidebar.slider("📈 Years Ahead for Inflation Adjustment", 0, 10, 3)
travel_date = st.sidebar.date_input("📅 Select Travel Date", datetime.today())

# User-defined budget allocation
st.sidebar.subheader("📊 Adjust Your Budget Allocation")
flights_pct = st.sidebar.slider("✈️ Flights (%)", 10, 50, 30)
hotel_pct = st.sidebar.slider("🏨 Hotel (%)", 10, 50, 35)
food_pct = st.sidebar.slider("🍽️ Food (%)", 10, 30, 20)
activities_pct = 100 - (flights_pct + hotel_pct + food_pct)

# Compute Cost Breakdown
def get_cost_breakdown(budget, allocations):
    breakdown = np.array(allocations) * budget / 100
    return dict(zip(["Flights", "Hotel", "Food", "Activities"], breakdown))

def adjust_for_inflation(cost, years, rate=3):
    return cost * ((1 + rate / 100) ** years)

costs_now = get_cost_breakdown(budget, [flights_pct, hotel_pct, food_pct, activities_pct])
costs_future = {k: adjust_for_inflation(v, years_ahead) for k, v in costs_now.items()}

df = pd.DataFrame({"Category": costs_now.keys(), "Current Cost": costs_now.values(), "Future Cost": costs_future.values()})

# Display Cost Breakdown
st.title("✈️ Vacation Budget Planner")
st.subheader(f"📊 Estimated Costs for {destination} ({currency})")
st.dataframe(df.style.format({"Current Cost": "{:.2f}", "Future Cost": "{:.2f}"}))

# Visualization - Side-by-Side Bar Chart
st.subheader("📊 Cost Breakdown Chart")
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Category", sort=None),
    y=alt.Y("Current Cost", title=f"Cost ({currency})"),
    color=alt.Color("Category", scale=alt.Scale(scheme="tableau10")),
    tooltip=["Category", "Current Cost", "Future Cost"]
).properties(width=600, height=400)
st.altair_chart(chart, use_container_width=True)

# Visualization - Doughnut Chart
fig, ax = plt.subplots()
ax.pie(costs_now.values(), labels=costs_now.keys(), autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"], wedgeprops={'edgecolor': 'black'})
ax.add_artist(plt.Circle((0,0),0.5,fc='white'))  # Making it a Doughnut
st.subheader("🍩 Cost Distribution")
st.pyplot(fig)

# AI Travel Recommendations (Basic Static)
st.subheader("✈️ AI Suggested Destinations")
destination_suggestions = {
    "Budget": ["Bali", "Bangkok", "Vietnam"],
    "Mid-range": ["Spain", "Portugal", "Turkey"],
    "Luxury": ["Maldives", "Switzerland", "Dubai"]
}
st.write(f"Based on your budget & travel style, you might consider: **{', '.join(destination_suggestions[travel_style])}**")
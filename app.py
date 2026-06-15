import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "data", "superstore.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    print("Connected to database")
    return conn

st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Superstore Sales Dashboard")
st.markdown("Sales performance analysis across regions, products, and customers.")

@st.cache_data
def load_data():
    conn = get_connection()
    query = """
    SELECT * FROM superstore
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

st.sidebar.header("Filters")
regions = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    options=df['Order Year'].unique(),
    default=df['Order Year'].unique()
)

df_filtered = df[
    (df['Region'].isin(regions)) &
    (df['Order Year'].isin(year))
]

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.2f}")

with col2: st.metric("Total Orders", df_filtered['Order ID'].nunique())

with col3: st.metric("Total Customers", df_filtered['Customer ID'].nunique())

with col4: st.metric("Avg Order Value", f"${df_filtered['Sales'].mean():,.2f}")

# Revenue Trend Section

revenue_trend = df_filtered.groupby(['Order Year', 'Order Month'])['Revenue'].sum().reset_index()

# Combine Order Year and Order Month into a single datetime column so the x-axis renders correctl
revenue_trend['Date'] = pd.to_datetime(
    revenue_trend[['Order Year', 'Order Month']]
    .rename(columns={'Order Year': 'year', 'Order Month': 'month'})
    .assign(day=1) # pd.to_datetime needs a day value — we use 1 for the 1st of each month
)

st.markdown("---")
st.subheader("Revenue Trend")

fig = px.line(
    data_frame=revenue_trend, 
    x='Date', 
    y='Revenue', 
    title='Monthly Revenue Over Time', 
    labels={'Revenue': 'Total Revenue ($)'}
    )
st.plotly_chart(fig, use_container_width=True)

# Top Products Section
top_products = (df_filtered.groupby('Product Name')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False).head(10))
sales_by_region = (df_filtered.groupby('Region')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False))

st.markdown("---")
st.subheader("Product & Regional Performance")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        data_frame=top_products, 
        x='Revenue', 
        y='Product Name', 
        orientation='h',
        title='Top 10 Products by Revenue',
        labels= {'Revenue': 'Total Revenue ($)', 'Product Name': 'Product'},
        color='Product Name'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(
        data_frame=sales_by_region,
        x='Region',
        y='Revenue',
        title='Revenue by Region',
        color='Region'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Top Customers Section
customer_summary=df_filtered.groupby(
    ['Customer ID', 'Customer Name', 'Segment']
).agg(
    Total_Orders=('Order ID', 'nunique'),
    Total_Revenue=('Revenue', 'sum'),
    Avg_Order_Value=('Sales', 'mean')
).reset_index().sort_values(
    by='Total_Revenue', ascending=False
).head(20)

customer_summary['Total_Revenue'] = customer_summary['Total_Revenue'].round(2)
customer_summary['Avg_Order_Value'] = customer_summary['Avg_Order_Value'].round(2)

st.markdown("---")
st.subheader("Top 20 Customers")

st.dataframe(customer_summary, use_container_width=True)
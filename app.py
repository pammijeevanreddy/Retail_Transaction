import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

# =========================
# DATA LOADING + CLEANING
# =========================
@st.cache_data
def load_and_clean_data():

    df=pd.read_csv(r"C:\Users\91990\Downloads\dataset\data.csv")

    # --- Standardize column names ---
    df.columns = [c.strip() for c in df.columns]

    # Handle both "UnitPrice" and "Price"
    if "UnitPrice" in df.columns and "Price" not in df.columns:
        df = df.rename(columns={"UnitPrice": "Price"})
    if "InvoiceNo" in df.columns and "Invoice" not in df.columns:
        df = df.rename(columns={"InvoiceNo": "Invoice"})
    if "CustomerID" in df.columns and "Customer ID" not in df.columns:
        df = df.rename(columns={"CustomerID": "Customer ID"})

    # --- Basic cleaning ---
    # Drop fully empty rows
    df = df.dropna(how="all")

    # Drop rows missing key fields
    for col in ["Description", "Quantity", "Price"]:
        if col in df.columns:
            df = df.dropna(subset=[col])

    # Remove non-positive quantity/price
    if "Quantity" in df.columns:
        df = df[df["Quantity"] > 0]
    if "Price" in df.columns:
        df = df[df["Price"] > 0]

    # Parse InvoiceDate
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    # Create Revenue
    df["Revenue"] = df["Quantity"] * df["Price"]

    # --- Custom cleaning for non-product StockCodes/fees ---
    if "StockCode" in df.columns:
        non_products = [
            "AMAZONFEE",
            "ADJUST",
            "ADJUSTMENT",
            "BANK CHARGES",
            "POST",
        ]
        df = df[~df["StockCode"].astype(str).isin(non_products)]

    if "Description" in df.columns:
        df = df[~df["Description"].str.contains("fee|charge|adjust", case=False, na=False)]

    # Keep only alphanumeric StockCodes, length > 2
    if "StockCode" in df.columns:
        df = df[df["StockCode"].astype(str).str.match(r"^[A-Za-z0-9]+$")]
        df = df[df["StockCode"].astype(str).str.len() > 2]

    return df


df = load_and_clean_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

# Country filter
if "Country" in df.columns:
    countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries, index=0)
else:
    selected_country = "All"

# Date filter
if "InvoiceDate" in df.columns:
    min_date = df["InvoiceDate"].min().date()
    max_date = df["InvoiceDate"].max().date()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None

# Apply filters
filtered_df = df.copy()

if selected_country != "All" and "Country" in df.columns:
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if date_range is not None and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"].dt.date >= start_date) &
        (filtered_df["InvoiceDate"].dt.date <= end_date)
    ]

# =========================
# HEADER
# =========================
st.title("🛒 Retail Sales Analytics Dashboard")

if selected_country == "All":
    st.caption("Showing data for **all countries**")
else:
    st.caption(f"Showing data for **{selected_country}**")

# =========================
# KPI CARDS
# =========================
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["Invoice"].nunique() if "Invoice" in filtered_df.columns else np.nan
total_customers = filtered_df["Customer ID"].nunique() if "Customer ID" in filtered_df.columns else np.nan

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")

st.markdown("---")

# =========================
# MONTHLY REVENUE TREND
# =========================
st.subheader("📈 Monthly Revenue Trend")

if "Month" in filtered_df.columns:
    monthly_rev = (
        filtered_df.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    if not monthly_rev.empty:
        # Convert Month to datetime for proper plotting
        monthly_rev["Month_dt"] = pd.to_datetime(monthly_rev["Month"])

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(monthly_rev["Month_dt"], monthly_rev["Revenue"])
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        ax.set_title("Monthly Revenue")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No data available for selected filters.")
else:
    st.warning("Month column not available.")

st.markdown("---")

# =========================
# TOP 10 PRODUCTS
# =========================
st.subheader("🏆 Top 10 Products by Revenue")

if {"Description", "Revenue"}.issubset(filtered_df.columns):
    top_products = (
        filtered_df.groupby("Description")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    if not top_products.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(top_products["Description"], top_products["Revenue"])
        ax.set_xlabel("Revenue")
        ax.set_ylabel("Product")
        ax.set_title("Top 10 Products by Revenue")
        plt.gca().invert_yaxis()  # Highest at top
        st.pyplot(fig)

        st.dataframe(top_products)
    else:
        st.info("No product data for selected filters.")
else:
    st.warning("Product Description or Revenue column missing.")

st.markdown("---")

# =========================
# TOP 10 COUNTRIES
# =========================
st.subheader("🌍 Top 10 Countries by Revenue")

if {"Country", "Revenue"}.issubset(df.columns):
    # Note: use full df for overall ranking, not only filtered_df
    country_rev = (
        df.groupby("Country")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(country_rev["Country"], country_rev["Revenue"])
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Country")
    ax.set_title("Top 10 Countries by Revenue")
    plt.gca().invert_yaxis()
    st.pyplot(fig)

    st.dataframe(country_rev)
else:
    st.warning("Country or Revenue column missing.")

st.markdown("---")

# =========================
# ORDER VALUE DISTRIBUTION
# =========================ls
st.subheader("📦 Order Value Distribution")

if {"Invoice", "Revenue"}.issubset(filtered_df.columns):
    order_value = (
        filtered_df.groupby("Invoice")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "OrderValue"})
    )

    if not order_value.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(order_value["OrderValue"], bins=40)
        ax.set_xlabel("Order Value")
        ax.set_ylabel("Number of Orders")
        ax.set_title("Order Value Distribution")
        st.pyplot(fig)
    else:
        st.info("No orders for selected filters.")
else:
    st.warning("Invoice or Revenue column missing.")

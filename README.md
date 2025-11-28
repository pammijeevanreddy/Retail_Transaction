📊 Dataset Description

Typical columns in online_retail_II.xlsx:

Column	Description
InvoiceNo	Transaction ID
StockCode	Product code (SKU)
Description	Product name
Quantity	Quantity of items (can be negative)
InvoiceDate	Date & time of transaction
UnitPrice	Price per unit
CustomerID	Unique customer identifier
Country	Customer country

👉 Dataset may include:

Returns (negative quantities)

Fees / adjustments like AMAZONFEE, ADJUST, BANK CHARGES etc.

🧹 Data Cleaning Steps

The following cleaning logic is applied in app.py:

Standardize column names

UnitPrice → Price

InvoiceNo → Invoice

CustomerID → Customer ID

Remove invalid rows

Drop completely empty rows

Drop rows with missing Description, Quantity, or Price

Keep only rows where:

Quantity > 0

Price > 0

Convert dates and create Month

Convert InvoiceDate to datetime

Create Month column: YYYY-MM

Create Revenue

Revenue = Quantity * Price


Remove non-product rows

Remove rows where StockCode is one of:

AMAZONFEE, ADJUST, ADJUSTMENT, POST, BANK CHARGES

Remove rows where Description contains:

"fee", "charge", "adjust" (case-insensitive)

Keep only alphanumeric StockCode values with length > 2

This ensures analysis focuses only on real products and sales.

📈 Analysis & KPIs

The dashboard calculates and displays:

1️⃣ Key Metrics (KPIs)

Total Revenue – sum of all Revenue

Total Orders – count of unique Invoice

Unique Customers – count of unique Customer ID

2️⃣ Monthly Revenue Trend

Grouped by Month

Line chart showing revenue over time

Helps identify seasonality and peak months

3️⃣ Top 10 Products by Revenue

Grouped by Description

Sorted by Revenue (descending)

Horizontal bar chart + data table

4️⃣ Top 10 Countries by Revenue

Grouped by Country

Sorted by Revenue (descending)

Horizontal bar chart + data table

5️⃣ Order Value Distribution

Total revenue per Invoice

Histogram chart

Shows difference between small orders and high-value bulk orders

🖥️ Streamlit Dashboard – Main Pages

All in one page with sections:

Filters (Sidebar)

Country dropdown: All or specific country

Date range picker (start date → end date)

KPIs Section

Large cards for:

Total Revenue

Total Orders

Unique Customers

Monthly Revenue Chart

Line chart with Month vs Revenue

Top Products Section

Top 10 products by revenue

Horizontal bar chart + table

Top Countries Section

Top 10 countries by revenue

Horizontal bar chart + table

Order Value Distribution

Histogram of OrderValue (sum of revenue per invoice)

⚙️ Setup & Installation
1️⃣ Clone the repository (or create folder)
git clone https://github.com/<your-username>/retail_project.git
cd retail_project


Or just create a folder and place:

app.py

online_retail_II.xlsx

requirements.txt

2️⃣ Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On macOS / Linux

3️⃣ Install dependencies
pip install -r requirements.txt


Contents of requirements.txt:

pandas
numpy
matplotlib
seaborn
streamlit
openpyxl

4️⃣ Run the Streamlit app
streamlit run app.py


The dashboard will open in your browser at:

http://localhost:8501

🔍 Example Business Insights (You Can Customize)

You can mention insights like:

A small set of products generates a large share of total revenue (80/20 rule).

The UK contributes the highest revenue among all countries.

Certain months show much higher revenue, indicating strong seasonality.

Many customers purchase only once, while a few repeat customers contribute significantly more.

These can be used in:

Project report

Resume bullet points

Interview explanations

💼 What This Project Demonstrates

Ability to work with large, messy Excel datasets

Practical data cleaning and feature engineering

Understanding of retail KPIs and business logic

Building an interactive dashboard for non-technical users

Using Python + Streamlit as a lightweight BI/analytics solution

✅ How to Explain in Interview (Sample)

I built a retail analytics dashboard using Python and Streamlit on top of a 500k+ row transaction dataset.
I cleaned the data by removing invalid quantities, prices, and non-product rows like fees and adjustments.
I engineered a Revenue field and a Month field and then calculated KPIs for total revenue, orders, and customers.
In the dashboard, I show monthly revenue trends, top products, top countries, and order value distribution with interactive filters for country and date.
This project demonstrates my skills in data cleaning, analysis, and building end-to-end analytical solutions.

🙏 Acknowledgements

Dataset: Online Retail II (UCI / Kaggle) or provided Excel file

Tools: Streamlit, Pandas, Matplotlib, Seaborn


If you also want, I can give you the **exact `requirements.txt` and `app.py` again together** so you can zip the whole project and upload to GitHub.
::contentReference[oaicite:0]{index=0}

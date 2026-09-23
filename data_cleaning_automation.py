import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("Thiranex_Task4_Messy_Sales_Data.xlsx")

# Check original data
print(df.head())
print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())

# Rename columns
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Clean text
text_cols = ["customer_name", "city", "category", "product", "payment_mode"]

for col in text_cols:
    df[col] = df[col].astype("string").str.strip().str.title()

print("\nText cleaning completed!")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["order_date"] = df["order_date"].fillna(
    df["order_date"].mode()[0]
)

print("Invalid dates fixed!")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

print("Dates and numbers cleaned!")

df.loc[df["quantity"] <= 0, "quantity"] = np.nan
df.loc[df["unit_price"] <= 0, "unit_price"] = np.nan

df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())

print("Invalid values fixed!")

df["customer_name"] = df["customer_name"].fillna("Unknown")
df["city"] = df["city"].fillna("Unknown")
df["payment_mode"] = df["payment_mode"].fillna("Unknown")

print("Missing text values fixed!")

df = df.drop_duplicates()

print("Duplicate rows removed!")

df["sales"] = df["quantity"] * df["unit_price"]

print("Sales column fixed!")

print("\nAFTER CLEANING")
print("Rows:", len(df))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

df["category"] = df["category"].replace({
    "Cloth": "Clothing",
    "Elec": "Electronics"
})

print("Category names standardized!")
summary = df.groupby("category")["sales"].sum().reset_index()

print("\nSALES SUMMARY")
print(summary)
summary.plot(x="category", y="sales", kind="bar", legend=False)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()
plt.savefig("sales_by_category.png")
plt.close()

print("Sales chart created!")

df["month"] = df["order_date"].dt.to_period("M").astype(str)

monthly = df.groupby("month")["sales"].sum()

monthly.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.tight_layout()
plt.savefig("monthly_sales_trend.png")
plt.close()

print("Monthly sales chart created!")
df.to_excel("cleaned_sales_data.xlsx", index=False)

print("Cleaned Excel file created!")
with pd.ExcelWriter("automated_report.xlsx") as writer:
    df.to_excel(writer, sheet_name="Cleaned Data", index=False)
    summary.to_excel(writer, sheet_name="Sales Summary", index=False)

print("Automated report created!")
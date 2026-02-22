import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set visual style
sns.set_theme(style="whitegrid")

# STEP 1: Load the CSV file
df = pd.read_csv("random_sales_data_10000_rows.csv")

# STEP 2: Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# STEP 3: Create Month column and sort
df['Month'] = df['Date'].dt.to_period('M')
df = df.sort_values('Date')

# ======================================
# Monthly Sales Trend
# ======================================
monthly_sales = df.groupby('Month')['Quantity'].sum().reset_index()
# Convert Month back to timestamp for plotting compatibility
monthly_sales['Month_Timestamp'] = monthly_sales['Month'].dt.to_timestamp()

print("\n" + "="*30)
print("   MONTHLY SALES TOTALS   ")
print("="*30)
print(monthly_sales[['Month', 'Quantity']].to_string(index=False))

plt.figure(figsize=(10, 6))
plt.plot(monthly_sales['Month_Timestamp'], monthly_sales['Quantity'], marker='o', linestyle='-', color='b', linewidth=2)
plt.title("Monthly Sales Trend", fontsize=14, fontweight='bold')
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Quantity Sold", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("monthly_sales_trend.png")
print("\n[Saved: monthly_sales_trend.png]")

# ======================================
# Best and Worst Months
# ======================================
best_month = monthly_sales.loc[monthly_sales['Quantity'].idxmax()]
worst_month = monthly_sales.loc[monthly_sales['Quantity'].idxmin()]

print("\n" + "="*30)
print("     INSIGHTS             ")
print("="*30)
print(f"Best Month:  {best_month['Month']} ({best_month['Quantity']} units)")
print(f"Worst Month: {worst_month['Month']} ({worst_month['Quantity']} units)")

# ======================================
# Sales by Region
# ======================================
region_sales = df.groupby('Region')['Quantity'].sum().sort_values(ascending=False).reset_index()

print("\n" + "="*30)
print("     SALES BY REGION      ")
print("="*30)
print(region_sales.to_string(index=False))

plt.figure(figsize=(8, 6))
sns.barplot(data=region_sales, x='Region', y='Quantity', palette='viridis')
plt.title("Total Sales by Region", fontsize=14, fontweight='bold')
plt.xlabel("Region", fontsize=12)
plt.ylabel("Total Quantity Sold", fontsize=12)
plt.tight_layout()
plt.savefig("sales_by_region.png")
print("\n[Saved: sales_by_region.png]")

# ======================================
# Generate Report
# ======================================
total_quantity = df['Quantity'].sum()
top_region = region_sales.iloc[0]['Region']
top_region_value = region_sales.iloc[0]['Quantity']

report_path = "sales_report.md"
if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace("[Pending Update]", str(best_month['Month']), 1)
    content = content.replace("[Pending Update]", f"{best_month['Quantity']} units", 1)
    content = content.replace("[Pending Update]", str(worst_month['Month']), 1)
    content = content.replace("[Pending Update]", f"{worst_month['Quantity']} units", 1)
    content = content.replace("[Pending Update]", f"{total_quantity:,} units", 1)
    content = content.replace("[Pending Update]", f"{total_quantity:,} units", 1) # Total Units Sold Details
    content = content.replace("[Pending Update]", top_region, 1)
    content = content.replace("[Pending Update]", f"Strengthen marketing in {top_region} ({top_region_value} units)", 1)
    
    # Update timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    content = content.replace("Report generated on: 2026-02-22", f"Report generated on: {today}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n[Updated: {report_path}]")

print("\nProcessing Complete.")
# plt.show() # Commented out for automated execution consistency

# Power BI Integration Guide - Monthly Sales Trends

Follow these steps to import the sales data and replicate the analysis within Power BI.

## Method 1: Direct CSV Import (Recommended)

1. Open **Power BI Desktop**.
2. Click on **Get Data** > **Text/CSV**.
3. Navigate to and select: `d:\sales-analysis-project\sales-analysis-project\random_sales_data_10000_rows.csv`.
4. Click **Load**.
5. **Create the visuals**:
   - **Monthly Trend**: Drag `Date` to the X-axis and `Quantity` to the Y-axis. Change the visual type to **Line Chart**.
   - **Regional Sales**: Drag `Region` to the X-axis and `Quantity` to the Y-axis. Change the visual type to **Clustered Bar Chart**.

## Method 2: Python Script Import

Use this method if you want to include the pre-processed date columns (Year, MonthYear, DayOfWeek) calculated in Python.

1. Open **Power BI Desktop**.
2. Click on **Get Data** > **More...** > **Other** > **Python script**.
3. Copy and paste the contents of `powerbi_script.py`:
   ```python
   import pandas as pd
   df = pd.read_csv(r"d:\sales-analysis-project\sales-analysis-project\random_sales_data_10000_rows.csv")
   df['Date'] = pd.to_datetime(df['Date'])
   df['Year'] = df['Date'].dt.year
   df['MonthYear'] = df['Date'].dt.to_period('M').astype(str)
   df['DayOfWeek'] = df['Date'].dt.day_name()
   sales_data = df
   ```
4. Click **OK**.
5. In the **Navigator** window, check the box next to `sales_data` and click **Load**.

## Dashboard Suggestions

- **Slicer**: Add a Slicer visual for `Region` to filter the entire dashboard.
- **KPI Cards**: Add a Card visual for `Sum of Quantity` to show total sales at a glance.
- **Top Month**: Use a Table visual sorted by `Quantity` descending to highlight the best month.

import pandas as pd
import os

# Define the absolute path to the dataset
# Note: For Power BI, it's often safer to use absolute paths or ensure the file is in the PBI working directory
dataset_path = r"d:\sales-analysis-project\sales-analysis-project\random_sales_data_10000_rows.csv"

# Load the dataset
df = pd.read_csv(dataset_path)

# Data Preprocessing
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['MonthNo'] = df['Date'].dt.month
df['MonthYear'] = df['Date'].dt.to_period('M').astype(str)
df['DayOfWeek'] = df['Date'].dt.day_name()

# This 'df' variable will be available as a table in Power BI
# We can also perform some aggregations here if needed, but Power BI is better at dynamic aggregations.
# However, let's ensure the data types are clean for import.

# Final cleaned dataframe for Power BI
sales_data = df.copy()
print("Data prepared for Power BI import.")

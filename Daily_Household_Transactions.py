import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings for cleaner output in a project context
import warnings
warnings.filterwarnings('ignore')

print("--- Project: Daily Household Transactions ---")

# --- Step 1: Import Libraries and Load Data ---
print("\nStep 1: Importing Libraries and Loading Data...")
try:
    df = pd.read_csv('Daily Household Transactions.csv')
    print("Dataset 'Daily Household Transactions.csv' loaded successfully.")
except FileNotFoundError:
    print("Error: 'Daily Household Transactions.csv' not found. Please ensure the file is in the correct directory.")
    exit() # Exit if the file is not found, as further steps depend on it

print("\nFirst 5 rows of the dataset:")
print(df.head())
print("\nDataset Info:")
df.info()
print("\nInitial Missing Values:")
print(df.isnull().sum())

# --- Step 2: Data Cleaning ---
print("\nStep 2: Data Cleaning...")

# Convert 'Date' column to datetime objects
# The date format in the file is 'DD/MM/YYYY HH:MM:SS' or 'DD/MM/YYYY'
# Using infer_datetime_format=True can help pandas automatically detect the format
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce')
print(f"Date column converted to datetime. New Dtype: {df['Date'].dtype}")

# Handle missing values
# As per the PDF example's data structure, 'Subcategory' and 'Note' have missing values.
# The PDF suggests filling 'Category' with 'Unknown', but our dataset has missing in 'Subcategory' and 'Note'.
df['Subcategory'].fillna('Unknown', inplace=True)
df['Note'].fillna('No Note', inplace=True)
print("\nMissing values after filling 'Subcategory' and 'Note':")
print(df.isnull().sum())

# Ensure 'Amount' is numeric (it's already float64, but good to ensure no non-numeric values snuck in)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
# If any NaN were introduced by coerce, fill them with the mean or median
if df['Amount'].isnull().any():
    mean_amount = df['Amount'].mean()
    df['Amount'].fillna(mean_amount, inplace=True)
    print(f"Filled missing/non-numeric 'Amount' values with mean: {mean_amount:.2f}")

# Remove duplicates
initial_rows = df.shape[0]
df.drop_duplicates(inplace=True)
rows_after_dedup = df.shape[0]
print(f"Removed {initial_rows - rows_after_dedup} duplicate rows.")

print("\nData types after cleaning:")
print(df.dtypes)
print("\nFirst 5 rows after cleaning:")
print(df.head())

# --- Step 3: Exploratory Data Analysis (EDA) ---
print("\nStep 3: Exploratory Data Analysis (EDA)...")

# Summary statistics
print("\nSummary Statistics for Numerical Columns:")
print(df.describe())

# Distribution of transaction amounts
plt.figure(figsize=(10, 6))
sns.histplot(df['Amount'], bins=50, kde=True)
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Amount (INR)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Transaction counts by Mode
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Mode', order=df['Mode'].value_counts().index)
plt.title('Transaction Counts by Mode of Payment')
plt.xlabel('Payment Mode')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Transaction counts by Category (top 10 for readability)
plt.figure(figsize=(14, 7))
top_categories = df['Category'].value_counts().index[:10]
sns.countplot(data=df, x='Category', order=top_categories)
plt.title('Top 10 Transaction Categories by Count')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Transaction counts by Income/Expense
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Income/Expense', order=df['Income/Expense'].value_counts().index)
plt.title('Transaction Counts by Income/Expense')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()

# Box plot of Amount by Category (top 5 for better visualization of outliers/spread)
plt.figure(figsize=(12, 8))
top_5_categories = df['Category'].value_counts().index[:5]
sns.boxplot(data=df[df['Category'].isin(top_5_categories)], x='Amount', y='Category', order=top_5_categories)
plt.title('Distribution of Amount by Top 5 Categories')
plt.xlabel('Amount (INR)')
plt.ylabel('Category')
plt.xscale('log') # Use log scale for amount due to wide range/outliers
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Box plot of Amount by Income/Expense
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Amount', y='Income/Expense')
plt.title('Distribution of Amount by Income/Expense Type')
plt.xlabel('Amount (INR)')
plt.ylabel('Income/Expense')
plt.xscale('log') # Use log scale for amount due to wide range/outliers
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- Step 4: Time Series Analysis ---
print("\nStep 4: Time Series Analysis...")

# Create 'YearMonth' and 'DayOfWeek' for further analysis
df['YearMonth'] = df['Date'].dt.to_period('M')
df['DayOfWeek'] = df['Date'].dt.day_name()

# Monthly trends of total amount
monthly_data = df.groupby('YearMonth')['Amount'].sum().to_frame().reset_index()
monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str) # Convert Period to string for plotting

plt.figure(figsize=(14, 7))
sns.lineplot(data=monthly_data, x='YearMonth', y='Amount', marker='o')
plt.title('Monthly Total Transaction Amounts')
plt.xlabel('Month')
plt.ylabel('Total Amount (INR)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Daily trends of total amount
daily_data = df.groupby(df['Date'].dt.date)['Amount'].sum().to_frame().reset_index()
daily_data['Date'] = pd.to_datetime(daily_data['Date']) # Convert back to datetime for proper plotting

plt.figure(figsize=(14, 7))
sns.lineplot(data=daily_data, x='Date', y='Amount', marker='o', linewidth=1)
plt.title('Daily Total Transaction Amounts')
plt.xlabel('Date')
plt.ylabel('Total Amount (INR)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- Step 5: Correlation Analysis ---
print("\nStep 5: Correlation Analysis (by category counts and average amounts)...")

# For correlation analysis between categories, it's more meaningful to look at:
# 1. Frequency of categories over time, or
# 2. Average/total amount spent per category.
# The PDF's example of pivot_table with 'Amount' and then .corr() assumes that the categories become
# numerical columns whose values can be correlated. This is not directly applicable if 'Category' itself is categorical.
# Instead, we can look at the average amount per category and see if there are relationships,
# or we can analyze the co-occurrence of categories if that's the intent.

# Let's pivot to analyze average amounts per category over time (e.g., by month)
# This will create a matrix where each column is a category and values are mean amounts.
df_monthly_category_avg = df.set_index('Date').groupby([pd.Grouper(freq='M'), 'Category'])['Amount'].mean().unstack(fill_value=0)

if not df_monthly_category_avg.empty and df_monthly_category_avg.shape[1] > 1:
    correlation_matrix_avg_amount = df_monthly_category_avg.corr()

    # Plot correlation heatmap for average amounts if there are enough categories
    if correlation_matrix_avg_amount.shape[0] > 1:
        plt.figure(figsize=(15, 12))
        sns.heatmap(correlation_matrix_avg_amount, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap of Monthly Average Transaction Amounts by Category')
        plt.tight_layout()
        plt.show()
        print("\nCorrelation matrix for monthly average transaction amounts by category:")
        print(correlation_matrix_avg_amount.head())
    else:
        print("\nNot enough categories or data points to generate a meaningful correlation heatmap for average amounts.")
else:
    print("\nCould not create a meaningful pivot table for correlation analysis of average amounts by category over time.")

print("\n--- Project Analysis Complete ---")

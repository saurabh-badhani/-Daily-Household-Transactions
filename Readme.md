# Daily Household Transactions Analysis 💰

This project analyzes a dataset of daily financial transactions to help understand personal spending patterns, income trends, and budgeting behavior.

---

## 🧾 Project Objectives

- Clean and process real-world-like financial transaction data.
- Explore income and expense trends across categories.
- Visualize payment modes, spending behavior, and income flow.
- Identify patterns for better financial planning.

---

## 📁 Dataset Overview

The dataset (`Daily Household Transactions.csv`) contains:

| Column           | Description                                      |
|------------------|--------------------------------------------------|
| Date             | Date & time of transaction                      |
| Mode             | Payment method (Cash, Bank, etc.)               |
| Category         | High-level expense/income category              |
| Subcategory      | Detailed category (e.g., Snacks, Fuel)          |
| Note             | Short transaction description                   |
| Amount           | Transaction amount in INR                       |
| Income/Expense   | Whether it's income or expense                  |
| Currency         | Currency used (INR)                             |

---

## 🧹 Data Cleaning Summary

- Converted `Date` column to datetime
- Filled missing values in `Subcategory` and `Note`
- Verified all amounts are numeric
- Removed 400+ duplicate entries

---

## 📊 Key Visualizations

- 📌 Distribution of transaction amounts
- 📌 Counts of payment modes
- 📌 Top categories and subcategories by frequency
- 📌 Income vs expense comparison
- 📌 Amount distribution across main categories
- 📌 Time-based trends (daily, monthly)
- 📌 Correlation heatmap of spending categories

---

## 🔍 How to Run This Project

1. Clone the repository:
```bash
git clone https://github.com/saurabh-badhani/Daily-Household-Transactions.git
cd Daily-Household-Transactions

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV file into a DataFrame with a corrected path
csv_file_path = r"D:\Hackbattle\Transactions.csv.txt"  # Use raw string for the path
transactions_df = pd.read_csv(csv_file_path)

# Print column names to debug
print("Columns in DataFrame:", transactions_df.columns)

# Strip any leading or trailing spaces from column names
transactions_df.columns = transactions_df.columns.str.strip()

# Convert the 'Date' column to datetime format (case-sensitive)
if 'Date' in transactions_df.columns:
    transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])
else:
    print("Error: 'Date' column not found in the DataFrame.")
    exit()  # Exit if the column is not found

# Function to plot pie chart
def plot_pie_chart(data, title):
    plt.figure(figsize=(8, 6))
    plt.pie(data['Total_Spending'], labels=data['Category'], autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
    plt.show()

# 1. Analyze the whole dataset for expenditure patterns
overall_analysis = transactions_df.groupby('Category')['Amount'].agg(['sum', 'mean']).reset_index()
overall_analysis.columns = ['Category', 'Total_Spending', 'Average_Spending']

print("\nOverall Expenditure Patterns:")
print(overall_analysis)

# Get the current month and last two months period
current_month_period = pd.Period(datetime.now().strftime('%Y-%m'))
last_month_period = pd.Period((datetime.now() - pd.DateOffset(months=1)).strftime('%Y-%m'))

# 2. Filter transactions for the current month, last month, and the past year
current_month_transactions = transactions_df[transactions_df['Date'].dt.to_period('M') == current_month_period]
last_month_transactions = transactions_df[transactions_df['Date'].dt.to_period('M') == last_month_period]

# Prompt the user for additional pie chart options
show_past_n_months = input("Do you want to see the spending distribution for the past n months? (yes/no): ").strip().lower()

# Plot pie chart for the current month
current_month_analysis = current_month_transactions.groupby('Category')['Amount'].agg(['sum']).reset_index()
current_month_analysis.columns = ['Category', 'Total_Spending']
plot_pie_chart(current_month_analysis, "Spending Distribution for Current Month")

# Optionally plot pie chart for last month

last_month_analysis = last_month_transactions.groupby('Category')['Amount'].agg(['sum']).reset_index()
last_month_analysis.columns = ['Category', 'Total_Spending']
plot_pie_chart(last_month_analysis, "Spending Distribution for Last Month")

# Optionally plot pie chart for past n months
if show_past_n_months == 'yes':
    n_months = int(input("Enter the number of past months to analyze: "))
    past_n_months_period = pd.Period((datetime.now() - pd.DateOffset(months=n_months)).strftime('%Y-%m'))
    past_n_months_transactions = transactions_df[transactions_df['Date'].dt.to_period('M') >= past_n_months_period]

    past_n_months_analysis = past_n_months_transactions.groupby('Category')['Amount'].agg(['sum']).reset_index()
    past_n_months_analysis.columns = ['Category', 'Total_Spending']
    plot_pie_chart(past_n_months_analysis, f"Spending Distribution for Past {n_months} Months")

# 4. Calculate total spending for the last month
total_spending_last_month = last_month_transactions['Amount'].sum()

# Add a new row for the total spending category
total_row = pd.DataFrame({
    'Category': ['Total Spending per Month'],
    'Total_Spending': [total_spending_last_month],
    'Average_Spending': [total_spending_last_month / len(last_month_transactions) if not last_month_transactions.empty else 0]
})

# Append the total spending row to the monthly category analysis
monthly_category_analysis = pd.concat([last_month_analysis, total_row], ignore_index=True)

# 5. Monitor current status of budget
budget_limit = float(input("Enter your monthly budget limit: "))
current_status = budget_limit - total_spending_last_month
print(f"\nCurrent Status of Budget: {current_status} remaining from your budget.")

# Get user input for savings goal and time frame
try:
    savings_goal = float(input("Enter your total savings goal: "))
    time_frame_months = int(input("Enter the time frame in months to reach your goal: "))
except ValueError:
    print("Invalid input. Please enter numeric values for savings goal and time frame.")
    exit()

# Calculate monthly savings needed to reach the goal
monthly_savings_needed = savings_goal / time_frame_months

# 6. Calculate suggested savings based on total spending for each category
monthly_category_analysis['Suggested_Savings'] = monthly_category_analysis['Total_Spending'] * 0.2  # Default: 20% of spending

# Calculate estimated savings amount per category
monthly_category_analysis['Estimated_Savings'] = monthly_category_analysis['Total_Spending'] * 0.2  # 20% of Total Spending

# Provide recommendations based on spending and savings goals
def recommend_plan(row, monthly_savings):
    if row['Total_Spending'] > monthly_savings:
        return "Consider reducing expenses."
    elif row['Total_Spending'] <= monthly_savings * 1.5:
        return "Maintain current spending and save more."
    else:
        return "You're managing well; consider investing savings."

monthly_category_analysis['Recommendation'] = monthly_category_analysis.apply(recommend_plan, axis=1, monthly_savings=monthly_savings_needed)

# Display the personalized savings plan
print("\nPersonalized Monthly Savings Plan by Category for Last Month:")
print(monthly_category_analysis[['Category', 'Total_Spending', 'Estimated_Savings', 'Recommendation']])

# Optional: Save the personalized plan to a CSV
monthly_category_analysis.to_csv('personalized_monthly_savings_plan_last_month.csv', index=False)

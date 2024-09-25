import pandas as pd

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

# Calculate total and average spending per category (case-sensitive)
category_analysis = transactions_df.groupby('Category')['Amount'].agg(['sum', 'mean']).reset_index()
category_analysis.columns = ['Category', 'Total_Spending', 'Average_Spending']

# Get user input for savings goal and time frame
savings_goal = float(input("Enter your total savings goal: "))
time_frame_months = int(input("Enter the time frame in months to reach your goal: "))

# Calculate monthly savings needed to reach the goal
monthly_savings_needed = savings_goal / time_frame_months
category_analysis['Suggested_Savings'] = category_analysis['Total_Spending'] * 0.2  # Default: 20% of spending

# Provide recommendations based on user input
def recommend_plan(row, monthly_savings):
    if row['Total_Spending'] > monthly_savings:
        return "Consider reducing expenses."
    elif row['Total_Spending'] <= monthly_savings * 1.5:
        return "Maintain current spending and save more."
    else:
        return "You're managing well; consider investing savings."

category_analysis['Recommendation'] = category_analysis.apply(recommend_plan, axis=1, monthly_savings=monthly_savings_needed)

# Display the personalized savings plan
print("\nPersonalized Savings Plan by Category:")
print(category_analysis)

# Optional: Save the personalized plan to a CSV
category_analysis.to_csv('personalized_savings_plan.csv', index=False)

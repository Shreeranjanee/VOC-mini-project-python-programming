import json
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt  # For optional plotting (ensure matplotlib is installed)

# Load expenses from a file (JSON format)
def load_from_file(filename='expenses.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if no file exists

# Save expenses to a file (JSON format)
def save_to_file(expenses, filename='expenses.json'):
    with open(filename, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense to the tracker
def add_expense(expenses):
    try:
        # Gather user input for expense details
        amount = float(input("Enter expense amount: $"))
        category = input("Enter category (e.g., Food, Transport, Entertainment): ")
        date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

        # If no date provided, use today's date
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Create an expense record
        expense = {
            "amount": amount,
            "category": category,
            "date": date
        }
        
        # Add to the expenses list and save to file
        expenses.append(expense)
        save_to_file(expenses)
        print("Expense added successfully!")
    
    except ValueError:
        print("Invalid input. Please enter a valid amount.")

# View summary of expenses (by category, overall, or time-based)
def view_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return

    summary_choice = input("View summary by: 1. Category 2. Overall 3. Time period\n")

    if summary_choice == '1':
        # View total spending by category
        category = input("Enter category: ")
        total = sum(exp['amount'] for exp in expenses if exp['category'].lower() == category.lower())
        print(f"Total spent on {category}: ${total:.2f}")
    
    elif summary_choice == '2':
        # View total spending overall
        total = sum(exp['amount'] for exp in expenses)
        print(f"Total spent overall: ${total:.2f}")
    
    elif summary_choice == '3':
        # View spending over a specific time period (daily, weekly, monthly)
        period_choice = input("Choose: 1. Daily 2. Weekly 3. Monthly\n")
        spending = defaultdict(float)

        for exp in expenses:
            exp_date = datetime.strptime(exp['date'], '%Y-%m-%d')
            if period_choice == '1':
                period = exp_date.strftime('%Y-%m-%d')  # Daily summary
            elif period_choice == '2':
                period = exp_date.strftime('%Y-%W')  # Weekly summary
            elif period_choice == '3':
                period = exp_date.strftime('%Y-%m')  # Monthly summary
            
            spending[period] += exp['amount']
        
        for period, total in spending.items():
            print(f"{period}: ${total:.2f}")
    
    else:
        print("Invalid option.")

# Bonus: Plot the spending by category using a pie chart
def plot_spending_by_category(expenses):
    categories = defaultdict(float)

    for exp in expenses:
        categories[exp['category']] += exp['amount']
    
    labels = list(categories.keys())
    amounts = list(categories.values())
    
    plt.pie(amounts, labels=labels, autopct='%1.1f%%')
    plt.title("Spending by Category")
    plt.show()

# User menu for interacting with the tracker
def menu():
    # Load existing expenses from file
    expenses = load_from_file()
    
    while True:
        # Display menu options
        print("\n1. Add Expense\n2. View Summary\n3. Plot Expenses by Category (Optional)\n4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            # Add a new expense
            add_expense(expenses)
        elif choice == '2':
            # View summary of expenses
            view_summary(expenses)
        elif choice == '3':
            # Plot spending by category (optional)
            plot_spending_by_category(expenses)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    menu()

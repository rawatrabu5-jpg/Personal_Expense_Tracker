"""
Personal Expense Tracker
Major Python Project

Features:
1. Add expenses
2. View all expenses
3. Categorize expenses
4. Generate reports
5. Save/load expenses using CSV
6. Visualize spending using Matplotlib
7. Error and exception handling
"""

import csv
import os
from datetime import datetime
from collections import defaultdict

CSV_FILE = "expenses.csv"


def load_expenses():
    """Load saved expenses from the CSV file."""
    expenses = []

    if not os.path.exists(CSV_FILE):
        return expenses

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    expenses.append({
                        "amount": float(row["amount"]),
                        "category": row["category"],
                        "date": row["date"],
                        "description": row["description"]
                    })
                except (ValueError, KeyError):
                    # Skip invalid rows instead of stopping the program.
                    continue

    except OSError as error:
        print(f"Error loading expenses: {error}")

    return expenses


def save_expenses(expenses):
    """Save all expenses to the CSV file."""
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["amount", "category", "date", "description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(expenses)

        print(f"\nExpenses saved successfully to {CSV_FILE}.")

    except OSError as error:
        print(f"\nError saving expenses: {error}")


def get_amount():
    """Get a valid positive expense amount."""
    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_date():
    """Get a valid date in YYYY-MM-DD format."""
    while True:
        date_text = input(
            "Enter date (YYYY-MM-DD), or press Enter for today: "
        ).strip()

        if date_text == "":
            return datetime.now().strftime("%Y-%m-%d")

        try:
            date = datetime.strptime(date_text, "%Y-%m-%d")
            return date.strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date. Example: 2026-09-27")


def get_category():
    """Get an expense category."""
    categories = [
        "Food",
        "Transport",
        "Entertainment",
        "Education",
        "Shopping",
        "Bills",
        "Health",
        "Other"
    ]

    print("\nCategories:")
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            choice = int(input("Choose category: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Please choose a valid category number.")

        except ValueError:
            print("Please enter a number.")


def add_expense(expenses):
    """Add a new expense."""
    print("\n========== ADD EXPENSE ==========")

    amount = get_amount()
    category = get_category()
    date = get_date()
    description = input("Enter description (optional): ").strip()

    expense = {
        "amount": amount,
        "category": category,
        "date": date,
        "description": description
    }

    expenses.append(expense)

    print("\nExpense added successfully!")


def view_expenses(expenses):
    """Display all expenses."""
    print("\n========== ALL EXPENSES ==========")

    if not expenses:
        print("No expenses recorded.")
        return

    print("-" * 78)
    print(f"{'No.':<5}{'Date':<15}{'Category':<20}{'Amount':<15}{'Description'}")
    print("-" * 78)

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number:<5}"
            f"{expense['date']:<15}"
            f"{expense['category']:<20}"
            f"₹{expense['amount']:<14.2f}"
            f"{expense['description']}"
        )

    print("-" * 78)
    print(f"Total expenses: {len(expenses)}")


def category_report(expenses):
    """Show total spending by category."""
    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]

    print("\n========== CATEGORY-WISE REPORT ==========")

    if not totals:
        print("No expenses recorded.")
        return totals

    grand_total = sum(totals.values())

    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        percentage = (amount / grand_total) * 100
        print(f"{category:<20} ₹{amount:>10.2f}  ({percentage:.1f}%)")

    print("-" * 45)
    print(f"{'Total':<20} ₹{grand_total:>10.2f}")

    return totals


def generate_report(expenses):
    """Generate overall spending reports."""
    print("\n========== EXPENSE REPORT ==========")

    if not expenses:
        print("No expenses recorded.")
        return

    total = sum(expense["amount"] for expense in expenses)
    average = total / len(expenses)
    highest = max(expenses, key=lambda expense: expense["amount"])

    print(f"Total spent       : ₹{total:.2f}")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Average expense   : ₹{average:.2f}")

    print("\nHighest expense:")
    print(f"  Amount      : ₹{highest['amount']:.2f}")
    print(f"  Category    : {highest['category']}")
    print(f"  Date        : {highest['date']}")
    print(f"  Description : {highest['description'] or 'N/A'}")

    category_report(expenses)


def monthly_report(expenses):
    """Show spending for each month."""
    monthly_totals = defaultdict(float)

    for expense in expenses:
        month = expense["date"][:7]  # YYYY-MM
        monthly_totals[month] += expense["amount"]

    print("\n========== MONTHLY REPORT ==========")

    if not monthly_totals:
        print("No expenses recorded.")
        return

    for month in sorted(monthly_totals):
        print(f"{month}: ₹{monthly_totals[month]:.2f}")


def visualize_expenses(expenses):
    """Create a bar chart and pie chart using Matplotlib."""
    if not expenses:
        print("\nNo expenses available for visualization.")
        return

    try:
        import matplotlib.pyplot as plt

        totals = defaultdict(float)

        for expense in expenses:
            totals[expense["category"]] += expense["amount"]

        categories = list(totals.keys())
        amounts = list(totals.values())

        # Bar chart
        plt.figure(figsize=(9, 5))
        plt.bar(categories, amounts)
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

        # Pie chart
        plt.figure(figsize=(7, 7))
        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Expense Distribution by Category")
        plt.tight_layout()
        plt.show()

    except ImportError:
        print("\nMatplotlib is not installed.")
        print("Install it using: pip install matplotlib")


def search_by_category(expenses):
    """Display expenses belonging to a selected category."""
    if not expenses:
        print("\nNo expenses recorded.")
        return

    category = get_category()

    matching = [
        expense for expense in expenses
        if expense["category"] == category
    ]

    print(f"\n========== {category.upper()} EXPENSES ==========")

    if not matching:
        print("No expenses found in this category.")
        return

    total = 0

    for number, expense in enumerate(matching, start=1):
        amount = expense["amount"]
        total += amount

        print(
            f"{number}. {expense['date']} | "
            f"₹{amount:.2f} | "
            f"{expense['description'] or 'No description'}"
        )

    print(f"\nTotal spent on {category}: ₹{total:.2f}")


def display_menu():
    """Display the main menu."""
    print("\n")
    print("=" * 45)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 45)
    print("1. Add an Expense")
    print("2. View All Expenses")
    print("3. Generate Report")
    print("4. Monthly Report")
    print("5. Search by Category")
    print("6. Visualize Expenses")
    print("7. Save and Exit")
    print("=" * 45)


def main():
    """Main program."""
    expenses = load_expenses()

    print("\nWelcome to Personal Expense Tracker!")

    if expenses:
        print(f"{len(expenses)} saved expense(s) loaded.")
    else:
        print("No previous expenses found.")

    while True:
        display_menu()

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_expense(expenses)

            elif choice == 2:
                view_expenses(expenses)

            elif choice == 3:
                generate_report(expenses)

            elif choice == 4:
                monthly_report(expenses)

            elif choice == 5:
                search_by_category(expenses)

            elif choice == 6:
                visualize_expenses(expenses)

            elif choice == 7:
                save_expenses(expenses)
                print("Thank you for using Personal Expense Tracker!")
                break

            else:
                print("Invalid choice. Please choose 1-7.")

        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

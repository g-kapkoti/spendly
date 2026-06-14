#!/usr/bin/env python3
"""Seed realistic dummy expenses for a specific user."""

import sys
import os
import random
from datetime import datetime, timedelta

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db

# Category definitions with Indian context and amount ranges (in ₹)
CATEGORIES = {
    "Food": {"min": 50, "max": 800, "weight": 30, "descriptions": [
        "Lunch at local dhaba", "Street food - pani puri", "Groceries from market",
        "Dinner at restaurant", "Morning chai and snacks", "Office tiffin",
        "Biryani takeaway", "South Indian thali", "Pizza delivery", "Bakery items"
    ]},
    "Transport": {"min": 20, "max": 500, "weight": 20, "descriptions": [
        "Auto rickshaw fare", "Metro card recharge", "Uber/Ola ride",
        "Bus pass monthly", "Fuel refill", "Taxi to airport",
        "Local train ticket", "Bike parking", "Car wash"
    ]},
    "Bills": {"min": 200, "max": 3000, "weight": 15, "descriptions": [
        "Electricity bill", "Mobile postpaid", "Internet broadband",
        "Water bill", "Cooking gas refill", "Credit card payment",
        "Rent contribution", "Society maintenance"
    ]},
    "Health": {"min": 100, "max": 2000, "weight": 8, "descriptions": [
        "Pharmacy medicines", "Doctor consultation", "Gym membership",
        "Health checkup", "Yoga class", "Medical test",
        "Physiotherapy session", "Vitamins supplement"
    ]},
    "Entertainment": {"min": 100, "max": 1500, "weight": 10, "descriptions": [
        "Movie tickets", "Netflix subscription", "Concert entry",
        "Gaming subscription", "Book purchase", "Amusement park",
        "Sports event ticket", "Music streaming"
    ]},
    "Shopping": {"min": 200, "max": 5000, "weight": 12, "descriptions": [
        "Clothes from mall", "Shoes purchase", "Mobile accessories",
        "Home decor items", "Kitchen appliances", "Gift items",
        "Cosmetics", "Electronics gadget"
    ]},
    "Other": {"min": 50, "max": 1000, "weight": 5, "descriptions": [
        "Gift for friend", "Donation", "Stationery",
        "Pet supplies", "Gardening items", "Miscellaneous"
    ]}
}


def parse_args():
    """Parse command line arguments."""
    if len(sys.argv) != 4:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        count = int(sys.argv[2])
        months = int(sys.argv[3])
        return user_id, count, months
    except ValueError:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        print("Error: All arguments must be valid integers.")
        sys.exit(1)


def verify_user(user_id):
    """Verify that the user exists in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print(f"No user found with id {user_id}.")
        sys.exit(1)

    return user


def generate_expenses(user_id, count, months):
    """Generate expense records spread across the specified months."""
    expenses = []

    # Build weighted category list
    category_list = []
    for cat, data in CATEGORIES.items():
        category_list.extend([cat] * data["weight"])

    today = datetime.now()

    for _ in range(count):
        # Pick random category based on weights
        category = random.choice(category_list)
        cat_data = CATEGORIES[category]

        # Generate random amount within range
        amount = round(random.uniform(cat_data["min"], cat_data["max"]), 2)

        # Generate random date within the past 'months' months
        days_ago = random.randint(0, months * 30)
        expense_date = today - timedelta(days=days_ago)
        date_str = expense_date.strftime("%Y-%m-%d")

        # Pick random description
        description = random.choice(cat_data["descriptions"])

        expenses.append((user_id, amount, category, date_str, description))

    return expenses


def insert_expenses(expenses):
    """Insert all expenses in a single transaction."""
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        sys.exit(1)
    finally:
        conn.close()


def confirm(user_id, count, months):
    """Print confirmation with stats and sample records."""
    conn = get_db()
    cursor = conn.cursor()

    # Get date range of inserted expenses
    cursor.execute(
        "SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?",
        (user_id,)
    )
    min_date, max_date = cursor.fetchone()

    # Get sample of 5 expenses
    cursor.execute(
        """SELECT id, amount, category, date, description
           FROM expenses WHERE user_id = ?
           ORDER BY RANDOM() LIMIT 5""",
        (user_id,)
    )
    samples = cursor.fetchall()

    conn.close()

    print(f"\nSuccessfully inserted {count} expenses for user {user_id}.")
    print(f"Date range: {min_date} to {max_date} ({months} months)")
    print(f"\nSample records:")
    print("-" * 80)
    for s in samples:
        print(f"  ID: {s['id']}, ₹{s['amount']:.2f}, {s['category']}, {s['date']}, {s['description']}")
    print("-" * 80)


def main():
    user_id, count, months = parse_args()

    user = verify_user(user_id)
    print(f"Found user: {user['name']} (ID: {user['id']})")

    expenses = generate_expenses(user_id, count, months)
    insert_expenses(expenses)
    confirm(user_id, count, months)


if __name__ == "__main__":
    main()

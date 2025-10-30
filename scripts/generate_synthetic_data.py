import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Config
START_DATE = datetime(2025, 8, 1)
END_DATE = datetime(2025, 10, 31)
OUTPUT_FILE = "scripts/sample_expenses.csv"

# Categories & keywords
CATEGORIES = {
    "Dining": ["McDonald's", "Chipotle", "Sushi Place", "Pizza Hut", "Dinner with friends", "Taco Bell"],
    "Coffee": ["Starbucks", "Dunkin", "Peet's Coffee", "Local Cafe"],
    "Transport": ["Uber", "Lyft", "Gas station", "Train ticket", "Parking", "Bus fare"],
    "Groceries": ["Whole Foods", "Trader Joe's", "Safeway", "Costco run", "Grocery trip"],
    "Entertainment": ["Netflix", "Movie theater", "Concert ticket", "Bowling", "Arcade"],
    "Other": ["Amazon purchase", "Pharmacy", "Haircut", "Gym membership", "Bookstore"]
}

# Budgets (for reference, not stored)
BUDGETS = {"Dining": 300, "Coffee": 80, "Transport": 150, "Groceries": 400, "Entertainment": 200}

# Generate random date
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# Generate expense
def generate_expense():
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=[20, 15, 18, 25, 12, 10],  # realistic frequency
        k=1
    )[0]
    
    description = random.choice(CATEGORIES[category])
    if "Starbucks" in description:
        amount = round(random.uniform(4.5, 7.5), 2)
    elif "Uber" in description or "Lyft" in description:
        amount = round(random.uniform(12, 45), 2)
    elif category == "Groceries":
        amount = round(random.uniform(40, 120), 2)
    elif category == "Dining":
        amount = round(random.uniform(15, 65), 2)
    elif category == "Entertainment" and "Netflix" in description:
        amount = 15.99
    else:
        amount = round(random.uniform(5, 50), 2)
    
    return {
        "date": random_date(START_DATE, END_DATE).strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
        "category": category  # we'll override with auto-categorizer later
    }

# Generate dataset
data = [generate_expense() for _ in range(140)]

df = pd.DataFrame(data)
df = df.sort_values("date").reset_index(drop=True)

# Create directory if not exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Generated {len(df)} synthetic expenses → {OUTPUT_FILE}")
print("\nPreview:")
print(df.head(10))
print(f"\nSpending by category:\n{df.groupby('category')['amount'].sum().round(2)}")
# scripts/generate_synthetic_data.py
import pandas as pd
import random
import os
from datetime import datetime, timedelta

# --- Configuration ---
START_DATE = datetime(2025, 8, 1)
END_DATE = datetime(2025, 12, 31)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../generated")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "sample_expenses_5months.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 50/30/20 Category Definitions ---
CATEGORIES = {
    # Needs (50%)
    "Groceries": ["Trader Joe's", "Whole Foods", "Safeway", "Walmart Grocery"],
    "Transport": ["Uber", "Lyft", "Gas Station", "Parking Meter", "Train Ticket"],

    # Wants (30%)
    "Dining": ["McDonald's", "Chipotle", "Taco Bell", "Olive Garden", "Local Diner"],
    "Coffee": ["Starbucks", "Dunkin'", "Peet's Coffee", "Local Cafe"],
    "Entertainment": ["Netflix", "Movie Theater", "Concert Ticket", "Spotify", "Bowling"],

    # Other (flexible)
    "Other": ["Amazon", "Target", "Bookstore", "Pharmacy", "Clothing Store"]
}

# Weights: Higher = more frequent
WEIGHTS = {
    "Groceries": 28,
    "Transport": 18,
    "Dining": 20,
    "Coffee": 15,
    "Entertainment": 12,
    "Other": 7
}

# --- Helper: Random date between START and END ---
def random_date():
    delta = (END_DATE - START_DATE).days
    random_days = random.randint(0, delta)
    return START_DATE + timedelta(days=random_days)

# --- Helper: Realistic amount by category ---
def random_amount(category: str) -> float:
    ranges = {
        "Groceries": (40, 120),
        "Transport": (8, 60),
        "Dining": (12, 45),
        "Coffee": (4, 8),
        "Entertainment": (10, 80),
        "Other": (15, 100)
    }
    low, high = ranges.get(category, (10, 50))
    return round(random.uniform(low, high), 2)

# --- Generate expense transactions ---
data = []
total_transactions = 300  # ~60 per month

for _ in range(total_transactions):
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=list(WEIGHTS.values()),
        k=1
    )[0]

    description = random.choice(CATEGORIES[category])
    amount = random_amount(category)
    date = random_date().date()

    data.append({
        "date": date,
        "description": description,
        "amount": amount,
        "category": category
    })

# --- Add Monthly Salary (Income) ---
current = START_DATE.replace(day=1)
while current <= END_DATE:
    salary_date = current.date()
    data.append({
        "date": salary_date,
        "description": "Monthly Salary",
        "amount": -5000.00,  # Negative = income
        "category": "Income"
    })
    # Move to next month
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1)
    else:
        current = current.replace(month=current.month + 1)

# --- Finalize and Save ---
df = pd.DataFrame(data)
df = df.sort_values("date").reset_index(drop=True)

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

# --- Summary ---
print(f"Generated {len(df)} transactions")
print(f"Date range: {df['date'].min()} → {df['date'].max()}")
print(f"Total spent: ${df[df['amount'] > 0]['amount'].sum():.2f}")
print(f"Total income: ${df[df['amount'] < 0]['amount'].abs().sum():.2f}")
print(f"Saved to: {OUTPUT_PATH}")
print("\nSample:")
print(df.head(10)[['date', 'description', 'amount', 'category']].to_string(index=False))
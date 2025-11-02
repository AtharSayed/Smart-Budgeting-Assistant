# scripts/ingest_csv.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from app.database import engine, create_db_and_tables
from app.models import Expense, Category, UserProfile
from app.categorizer import auto_categorize
from sqlalchemy import text
from sqlmodel import Session

CSV_PATH = r"E:\Technical-Seminar-II Project\Smart-Budgeting-Agent\generated\sample_expenses_5months.csv" # For local Build process

# --- Verify CSV exists ---
if not os.path.exists(CSV_PATH):
    print(f"ERROR: CSV not found at {CSV_PATH}")
    print("Run: python scripts/generate_synthetic_data.py")
    sys.exit(1)

print(f"Importing from: {CSV_PATH}")
print("Recreating database schema...")

# --- DROP & RECREATE SCHEMA (only on first run or when resetting) ---
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS expense"))
    conn.execute(text("DROP TABLE IF EXISTS category"))
    conn.execute(text("DROP TABLE IF EXISTS userprofile"))
    conn.execute(text("DROP TABLE IF EXISTS alembic_version"))

create_db_and_tables()
print("Database schema recreated.")

# --- Load & process CSV ---
df = pd.read_csv(CSV_PATH)
df["date"] = pd.to_datetime(df["date"]).dt.date
df = df.sort_values("date").reset_index(drop=True)

# --- Compute running balance ---
balance = 2000.0  # Starting balance
final_rows = []

for _, row in df.iterrows():
    balance -= row["amount"]  # income is negative → adds to balance
    row_dict = row.to_dict()
    row_dict["balance"] = round(balance, 2)
    final_rows.append(row_dict)

df = pd.DataFrame(final_rows)

# --- Insert expenses ---
with Session(engine) as session:
    for _, row in df.iterrows():
        category = "Income" if row["category"] == "Income" else auto_categorize(row["description"])
        expense = Expense(
            amount=row["amount"],
            description=row["description"],
            category=category,
            date=row["date"],
            balance=row["balance"]
        )
        session.add(expense)

    # --- Insert default UserProfile ---
    profile = UserProfile(name="Alex", monthly_income=5000.0, savings_goal=1000.0)
    session.add(profile)

    # --- Insert 50/30/20 Categories with budgets ---
    categories = [
        {"name": "Groceries",     "budget": 2500.0, "is_need": True,  "is_want": False, "is_saving": False},
        {"name": "Transport",     "budget": 500.0,  "is_need": True,  "is_want": False, "is_saving": False},
        {"name": "Dining",        "budget": 600.0,  "is_need": False, "is_want": True,  "is_saving": False},
        {"name": "Coffee",        "budget": 150.0,  "is_need": False, "is_want": True,  "is_saving": False},
        {"name": "Entertainment", "budget": 300.0,  "is_need": False, "is_want": True,  "is_saving": False},
        {"name": "Other",         "budget": 600.0,  "is_need": False, "is_want": True,  "is_saving": False},
        {"name": "Income",        "budget": 0.0,    "is_need": False, "is_want": False, "is_saving": False},
    ]

    for cat in categories:
        session.execute(
            text("""
            INSERT OR IGNORE INTO category 
            (name, budget, is_need, is_want, is_saving) 
            VALUES (:name, :budget, :is_need, :is_want, :is_saving)
            """),
            cat
        )

    session.commit()

print(f"SUCCESS: Imported {len(df)} records with running balances.")
print("50/30/20 budgets applied.")
print("Run: docker-compose up --build")
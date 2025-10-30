import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from app.database import get_session
from app.models import Expense
from app.categorizer import auto_categorize
from datetime import datetime

CSV_PATH = "data/sample_expenses.csv"

print("Importing expenses from CSV...")
df = pd.read_csv(CSV_PATH)

with next(get_session()) as session:
    # Clear old data (optional)
    session.exec("DELETE FROM expense")
    
    for _, row in df.iterrows():
        # Use auto-categorizer instead of CSV category
        category = auto_categorize(row['description'])
        expense = Expense(
            amount=row['amount'],
            description=row['description'],
            category=category,
            date=datetime.strptime(row['date'], "%Y-%m-%d").date()
        )
        session.add(expense)
    session.commit()

print(f"Imported {len(df)} expenses with auto-categorization!")
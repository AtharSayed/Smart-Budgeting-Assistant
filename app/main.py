from fastapi import FastAPI, Depends, UploadFile, Form, File
from sqlmodel import Session, select
from sqlalchemy import text  # ✅ added this
from .database import create_db_and_tables, get_session
from .context_manager import BudgetContext
from .models import Expense, UserProfile, Category
from .categorizer import auto_categorize
from .llm_handler import query_llm
import json
import shutil
import subprocess
import os
import pandas as pd
from datetime import datetime

app = FastAPI(title="Smart Budget Assistant")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    # ✅ safer way to seed default data
    with next(get_session()) as session:
        # check if Category table has data
        if not session.exec(select(Category)).first():
            session.add_all([
                Category(name="Dining", budget=300),
                Category(name="Transport", budget=150),
                Category(name="Entertainment", budget=200),
            ])
            session.add(UserProfile(name = "Default User",monthly_income=5000, savings_goal=1000))
            session.commit()

def build_prompt(user_query: str, context: dict) -> str:
    return f"""
You are a friendly, concise financial assistant.
Use this data:
- Monthly income: ${context['income']}
- Savings goal: ${context['savings_goal']}
- Current dining spent: ${context['dining_spent']:.2f} / ${context['dining_budget']}
- Can afford more dining: {'Yes' if context['can_afford_dining'] else 'No'}

User: {user_query}

Respond naturally and helpfully. Be proactive.
"""

@app.post("/ask")
async def ask(query: str, session: Session = Depends(get_session)):
    ctx = BudgetContext(session)

    # ✅ use model instead of raw SQL
    profile = session.exec(select(UserProfile)).first()

    dining_spent = ctx.get_monthly_spending("Dining")
    can_afford = ctx.can_afford(50, "Dining")  # assume $50 meal

    context = {
        "income": profile.monthly_income,
        "savings_goal": profile.savings_goal,
        "dining_spent": dining_spent,
        "dining_budget": ctx.get_budget_limit("Dining"),
        "can_afford_dining": can_afford
    }

    prompt = build_prompt(query, context)
    llm_response = query_llm(prompt)

    return {"response": llm_response, "context": context}

@app.get("/summary")
def get_summary(session: Session = Depends(get_session)):
    ctx = BudgetContext(session)
    cats = session.exec(select(Category)).all()
    data = {}
    for cat in cats:
        spent = ctx.get_monthly_spending(cat.name)
        data[cat.name] = {"spent": round(spent, 2), "budget": cat.budget}
    return data

@app.post("/ingest")
def ingest_csv(payload: dict, session: Session = Depends(get_session)):
    csv_path = payload["path"]
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        cat = auto_categorize(row["description"])
        exp = Expense(
            amount=row["amount"],
            description=row["description"],
            category=cat,
            date=datetime.strptime(row["date"], "%Y-%m-%d").date()
        )
        session.add(exp)
    session.commit()
    os.remove(csv_path)
    return {"status": "ok", "rows": len(df)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

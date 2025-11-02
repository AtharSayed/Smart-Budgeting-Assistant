# app/context_manager.py
from sqlmodel import Session, select
from app.database import engine
from app.models import Expense, Category, UserProfile
from datetime import datetime
from typing import Dict
from sqlalchemy import extract   # <-- NEW

class BudgetContext:
    def __init__(self):
        self.session = Session(engine)

    def __del__(self):
        self.session.close()

    # ------------------------------------------------------------------ #
    # Profile
    # ------------------------------------------------------------------ #
    def get_profile(self) -> UserProfile:
        profile = self.session.exec(select(UserProfile)).first()
        if not profile:
            profile = UserProfile(name="You", monthly_income=5000.0, savings_goal=1000.0)
            self.session.add(profile)
            self.session.commit()
        return profile

    # ------------------------------------------------------------------ #
    # Balance
    # ------------------------------------------------------------------ #
    def get_current_balance(self) -> float:
        latest = self.session.exec(select(Expense).order_by(Expense.id.desc())).first()
        return latest.balance if latest else 2000.0

    # ------------------------------------------------------------------ #
    # Monthly spending (fixed!)
    # ------------------------------------------------------------------ #
    def get_monthly_spending(self, category: str) -> float:
        now = datetime.now()
        expenses = self.session.exec(
            select(Expense).where(
                Expense.category == category,
                extract('month', Expense.date) == now.month,
                extract('year',  Expense.date) == now.year
            )
        ).all()
        return sum(e.amount for e in expenses if e.amount > 0)

    # ------------------------------------------------------------------ #
    # 50/30/20 breakdown
    # ------------------------------------------------------------------ #
    def get_503020_breakdown(self) -> Dict[str, float]:
        income = self.get_profile().monthly_income
        return {
            "needs": income * 0.5,
            "wants": income * 0.3,
            "savings": income * 0.2
        }

    # ------------------------------------------------------------------ #
    # Full 50/30/20 status
    # ------------------------------------------------------------------ #
    def get_spending_by_rule(self) -> Dict:
        breakdown = self.get_503020_breakdown()

        needs = sum(self.get_monthly_spending(c) for c in ["Groceries", "Transport"])
        wants = sum(self.get_monthly_spending(c) for c in ["Dining", "Coffee", "Entertainment"])
        savings_goal = self.get_profile().savings_goal   # you can track real savings later

        spent = {"needs": needs, "wants": wants, "savings": savings_goal}
        remaining = {k: breakdown[k] - spent[k] for k in breakdown}

        return {
            "limits": breakdown,
            "spent": spent,
            "remaining": remaining
        }
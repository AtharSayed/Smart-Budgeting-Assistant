# app/context_manager.py
from sqlmodel import select
from datetime import datetime
from .database import get_session
from .models import Expense, Category

class BudgetContext:
    def __init__(self, session):
        self.session = session

    def get_monthly_spending(self, category: str = None):
        first = datetime.now().replace(day=1)
        stmt = select(Expense).where(Expense.date >= first)
        if category:
            stmt = stmt.where(Expense.category == category)
        expenses = self.session.exec(stmt).all()
        return sum(e.amount for e in expenses)

    def get_budget_limit(self, category: str):
        cat = self.session.exec(select(Category).where(Category.name == category)).first()
        return cat.budget if cat else 100.0

    def can_afford(self, amount: float, category: str):
        spent = self.get_monthly_spending(category)
        limit = self.get_budget_limit(category)
        return spent + amount <= limit
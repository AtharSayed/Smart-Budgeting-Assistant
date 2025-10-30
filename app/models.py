# app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Category(SQLModel, table=True):
    name: str = Field(primary_key=True)
    budget: float = Field(default=100.0)

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: str = Field(foreign_key="category.name")
    date: date

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    monthly_income: float = Field(default=0.0)
    savings_goal: float = Field(default=0.0)
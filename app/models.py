from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Category(SQLModel, table=True):
    name: str = Field(primary_key=True)
    budget: float = Field(default=0.0)
    is_need: bool = Field(default=False)
    is_want: bool = Field(default=False)
    is_saving: bool = Field(default=False)

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: str = Field(foreign_key="category.name")
    date: date
    balance: float  # Running balance

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    monthly_income: float = Field(default=5000.0)
    savings_goal: float = Field(default=1000.0)
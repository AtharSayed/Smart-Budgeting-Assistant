from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from .database import get_session, create_db_and_tables
from .context_manager import BudgetContext
from .llm_handler import LLMHandler
from pydantic import BaseModel

app = FastAPI(title="Smart Budget Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
llm = LLMHandler()

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/ask")
def ask(request: QueryRequest, session: Session = Depends(get_session)):
    context = BudgetContext()
    response = llm.generate_response(request.query)
    return {
        "response": response,
        "budget_status": context.get_spending_by_rule(),
        "balance": context.get_current_balance(),
        "profile": {
            "income": context.get_profile().monthly_income,
            "savings_goal": context.get_profile().savings_goal
        }
    }

@app.get("/summary")
def summary():
    context = BudgetContext()
    return {
        "balance": context.get_current_balance(),
        "50_30_20": context.get_spending_by_rule(),
        "monthly_income": context.get_profile().monthly_income
    }
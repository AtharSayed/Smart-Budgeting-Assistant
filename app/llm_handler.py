import httpx
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.context_manager import BudgetContext

class LLMHandler:
    def __init__(self):
        # self.url = "http://ollama:11434/api/generate" # For containerized environment
        self.url = "http://localhost:11434/api/generate" # For local Build process
        self.model = "mistral:latest"

    def estimate_price(self, item: str) -> float:
        prices = {
            "coffee": 5.0, "dinner": 35.0, "uber": 22.0, "groceries": 80.0,
            "netflix": 15.99, "shirt": 45.0, "flight": 350.0
        }
        return prices.get(item.lower(), 50.0)

    def generate_response(self, query: str) -> str:
        context = BudgetContext()
        profile = context.get_profile()
        breakdown = context.get_503020_breakdown()
        spending = context.get_spending_by_rule()

        words = query.lower().split()
        item = next((w for w in words if w in self.estimate_price.__code__.co_varnames), None)
        est_price = self.estimate_price(item) if item else 0.0

        next_salary = (datetime.now().date().replace(day=1) + relativedelta(months=1))
        runway = max(1, (next_salary - datetime.now().date()).days)

        prompt = f"""
You are a 50/30/20 budgeting coach.

User: {query}
Item: {item or 'unknown'} (~${est_price:.2f})
Income: ${profile.monthly_income:.0f}
Balance: ${context.get_current_balance():.2f}
Days to salary: {runway}

50/30/20:
- Needs (50%): ${breakdown['needs']:.0f} → Spent ${spending['spent']['needs']:.0f}
- Wants (30%): ${breakdown['wants']:.0f} → Spent ${spending['spent']['wants']:.0f}
- Savings (20%): ${breakdown['savings']:.0f}

Rules:
- If >90% of bucket → "Cut back"
- Runway < 5 + high wants → "Wait"
- Suggest cheaper alternatives
- 1-2 sentences only
"""

        try:
            r = httpx.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False}, timeout=30)
            r.raise_for_status()
            return r.json().get("response", "Sorry, try again.").strip()
        except Exception:
            return "AI is offline. Try again later."
FOOD_KEYWORDS = ["restaurant", "cafe", "mcdonald", "chipotle", "taco", "dinner", "lunch"]
COFFEE_KEYWORDS = ["starbucks", "dunkin", "coffee"]
TRANSPORT_KEYWORDS = ["uber", "lyft", "gas", "parking", "train"]
GROCERY_KEYWORDS = ["trader joe", "whole foods", "grocery", "supermarket"]
ENTERTAINMENT_KEYWORDS = ["netflix", "concert", "movie", "spotify"]
INCOME_KEYWORDS = ["salary", "paycheck", "bonus"]

def auto_categorize(description: str) -> str:
    desc = description.lower()
    if any(k in desc for k in INCOME_KEYWORDS):
        return "Income"
    if any(k in desc for k in FOOD_KEYWORDS):
        return "Dining"
    if any(k in desc for k in COFFEE_KEYWORDS):
        return "Coffee"
    if any(k in desc for k in TRANSPORT_KEYWORDS):
        return "Transport"
    if any(k in desc for k in GROCERY_KEYWORDS):
        return "Groceries"
    if any(k in desc for k in ENTERTAINMENT_KEYWORDS):
        return "Entertainment"
    return "Other"
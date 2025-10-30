FOOD_KEYWORDS = ["restaurant", "cafe", "starbucks", "mcdonald", "dinner", "lunch"]
TRANSPORT_KEYWORDS = ["uber", "gas", "parking", "train"]

def auto_categorize(description: str) -> str:
    desc = description.lower()
    if any(k in desc for k in FOOD_KEYWORDS):
        return "Dining"
    if any(k in desc for k in TRANSPORT_KEYWORDS):
        return "Transport"
    return "Other"
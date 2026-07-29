import json
import os

# Helper to load data
def load_transactions():
    file_path = "enriched_statement 2.json"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as file:
        data = json.load(file)
        return data.get("transactions", [])

# Tool 1: Get recurring charges
def get_recurring_charges():
    """Returns a list of high-confidence recurring transactions or subscriptions."""
    transactions = load_transactions()
    recurring = [
        t for t in transactions 
        if t.get("recurring_candidate") and t.get("recurring_confidence", 0) >= 0.7
    ]
    return recurring

# Tool 2: Search transactions by location or category
def search_transactions(location=None, category=None):
    """Filters transactions by a specific location hint, merchant, raw description, or category."""
    transactions = load_transactions()
    results = transactions
    
    if location:
        loc_lower = location.lower()
        filtered = []
        for t in results:
            loc_hint = str(t.get("location_hint") or "").lower()
            merchant = str(t.get("merchant") or "").lower()
            desc = str(t.get("raw_description") or "").lower()
            
            # Check if location term matches location_hint, merchant name, or raw description text
            if loc_lower in loc_hint or loc_lower in merchant or loc_lower in desc:
                filtered.append(t)
        results = filtered

    if category:
        cat_lower = category.lower()
        results = [t for t in results if cat_lower in str(t.get("category", "")).lower()]
        
    return results

# Function dispatcher map
TOOL_MAP = {
    "get_recurring_charges": get_recurring_charges,
    "search_transactions": search_transactions,
}

# OpenAI Tool Definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_recurring_charges",
            "description": "Retrieves high-confidence recurring charges, subscriptions, and regular membership payments.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_transactions",
            "description": "Searches and filters transactions by location hint (e.g. 'Toronto', 'Manchester Airport') or category (e.g. 'Transport', 'Subscriptions', 'Dining').",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to filter by, e.g., 'Toronto' or 'Manchester'."
                    },
                    "category": {
                        "type": "string",
                        "description": "Category to filter by, e.g., 'Transport', 'Subscriptions', 'Financial Services', 'Dining'."
                    }
                },
                "required": []
            }
        }
    }
]
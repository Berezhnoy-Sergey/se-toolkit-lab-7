"""Basic command handlers with real backend integration."""
import asyncio
from services.api import BackendAPI

api = BackendAPI()

def start() -> str:
    return "Welcome to the LMS Bot! Use /help to see available commands."

def help() -> str:
    return """Available commands:
/start - welcome message
/help - this help
/health - check backend status
/labs - list available labs
/scores <lab> - per-task scores for a lab (e.g., /scores lab-04)"""

def health() -> str:
    try:
        items_count = asyncio.run(api.get_items_count())
        return f"✅ Backend is healthy. {items_count} items available."
    except Exception as e:
        return f"❌ Backend error: {str(e)}"

def labs() -> str:
    try:
        items = asyncio.run(api.get_items())
        # Filter only labs (type="lab")
        labs_list = [item for item in items if item.get("type") == "lab"]
        if not labs_list:
            return "No labs found in the database."
        result = "Available labs:\n"
        for lab in labs_list:
            result += f"- {lab['title']}\n"
        return result.strip()
    except Exception as e:
        return f"❌ Error fetching labs: {str(e)}"

def scores(lab: str) -> str:
    try:
        pass_rates = asyncio.run(api.get_pass_rates(lab))
        if not pass_rates:
            return f"No data found for {lab}."
        result = f"Pass rates for {lab}:\n"
        for task in pass_rates:
            task_name = task.get('task', 'Unknown')
            avg_score = task.get('avg_score', 0)
            attempts = task.get('attempts', 0)
            result += f"- {task_name}: {avg_score:.1f}% ({attempts} attempts)\n"
        return result.strip()
    except Exception as e:
        return f"❌ Error fetching scores for {lab}: {str(e)}"

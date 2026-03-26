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
        # Run async function in sync context
        is_healthy = asyncio.run(api.health_check())
        if is_healthy:
            return "✅ Backend is healthy."
        else:
            return "❌ Backend is not responding. Check if services are running."
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

def handle_text(message: str) -> str:
    """Handle natural language message via LLM."""
    import asyncio
    from services.llm import LLMClient
    from services.api import BackendAPI
    
    api = BackendAPI()
    llm = LLMClient()
    
    result = asyncio.run(llm.route(message))
    
    if result["tool"] == "get_labs":
        items = asyncio.run(api.get_items())
        labs = [item for item in items if item.get("type") == "lab"]
        if not labs:
            return "No labs found."
        response = "Available labs:\n"
        for lab in labs:
            response += f"- {lab['title']}\n"
        return response
    
    elif result["tool"] == "get_pass_rates":
        lab = result["args"].get("lab")
        if not lab:
            return "Please specify a lab, e.g., lab-04"
        pass_rates = asyncio.run(api.get_pass_rates(lab))
        if not pass_rates:
            return f"No data found for {lab}."
        response = f"Pass rates for {lab}:\n"
        for task in pass_rates:
            task_name = task.get('task', 'Unknown')
            avg_score = task.get('avg_score', 0)
            attempts = task.get('attempts', 0)
            response += f"- {task_name}: {avg_score:.1f}% ({attempts} attempts)\n"
        return response
    
    elif result["tool"] is None:
        return result.get("response", "I didn't understand that. Try asking about labs or scores.")
    
    return "Sorry, I couldn't process that."

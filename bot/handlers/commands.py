"""Basic command handlers."""

def start() -> str:
    return "Welcome to the LMS Bot! Use /help to see available commands."

def help() -> str:
    return "/start - welcome message\n/help - this help\n/health - check backend status\n/labs - list available labs\n/scores <lab> - per-task scores"

def health() -> str:
    return "Backend health check: placeholder (not yet implemented)"

def labs() -> str:
    return "Available labs: lab-01, lab-02, lab-03, lab-04, lab-05, lab-06"

def scores(lab: str) -> str:
    return f"Scores for {lab}: placeholder (not yet implemented)"

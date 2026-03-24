# Bot Development Plan

## Architecture
The bot is structured with:
- `bot.py` — entry point with `--test` mode
- `handlers/` — command handlers (to be implemented)
- `services/` — backend API client and LLM client

## Test Mode
The `--test` flag allows running commands without Telegram:
- Parses command line arguments
- Calls the same handler functions as Telegram mode
- Prints response to stdout

## Implementation Phases
1. Scaffold structure and test mode (Task 1)
2. Backend integration with real data (Task 2)
3. LLM-powered intent routing (Task 3)
4. Docker containerization (Task 4)

## Backend Integration Plan
- Use httpx for API calls
- Read LMS_API_KEY from environment
- Handle errors gracefully with user-friendly messages

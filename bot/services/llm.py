"""LLM client for intent routing."""
import os
import json
import httpx
from typing import List, Dict, Any

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env.bot.secret'))

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "coder-model")

# Tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_labs",
            "description": "Get list of all labs",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get pass rates for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-04'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores_distribution",
            "description": "Get score distribution for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are an assistant for a learning management system.
Your task is to route user questions to the appropriate tool.

IMPORTANT: You MUST use the tools. Do NOT answer questions yourself.

- If user asks about available labs → call get_labs
- If user asks about scores, pass rates, or task performance for a specific lab → call get_pass_rates with the lab parameter
- If user asks about score distribution → call get_scores_distribution

Examples:
- "what labs are available?" → get_labs()
- "show me scores for lab-04" → get_pass_rates(lab="lab-04")
- "lab 3 pass rates" → get_pass_rates(lab="lab-03")
- "score distribution lab 5" → get_scores_distribution(lab="lab-05")

If you cannot match to any tool, respond with "I didn't understand that. Try asking about labs or scores."
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_labs",
            "description": "Get list of all labs. Use this when user asks about available labs or what labs exist.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get pass rates (average score and attempts) for all tasks in a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-04'"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores_distribution",
            "description": "Get score distribution (4 buckets) for a lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    }
]

class LLMClient:
    async def route(self, message: str) -> Dict[str, Any]:
        """Route user message to appropriate tool."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{LLM_API_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                json={
                    "model": LLM_API_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": message}
                    ],
                    "tools": TOOLS,
                    "tool_choice": "auto"
                }
            )
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]
            message = choice["message"]
            
            if message.get("tool_calls"):
                tool_call = message["tool_calls"][0]
                return {
                    "tool": tool_call["function"]["name"],
                    "args": json.loads(tool_call["function"]["arguments"])
                }
            else:
                return {"tool": None, "response": message.get("content", "")}

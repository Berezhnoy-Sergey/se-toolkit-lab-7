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
            "description": "Get score distribution (4 buckets) for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of all learners (students)",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submission timeline for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top learners for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"},
                    "limit": {"type": "integer", "description": "Number of top learners", "default": 5}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL sync to refresh data from autochecker",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]


SYSTEM_PROMPT = """You are an assistant for a learning management system.
Your ONLY job is to route user questions to the correct tool.

IMPORTANT: You MUST call a tool. Do NOT answer questions yourself.

Available tools:
- get_labs(): List all labs
- get_pass_rates(lab): Pass rates for tasks in a lab
- get_learners(): List all learners (students)
- get_timeline(lab): Submission timeline for a lab
- get_groups(lab): Group performance for a lab
- get_top_learners(lab, limit): Top learners in a lab
- get_completion_rate(lab): Completion percentage for a lab
- trigger_sync(): Refresh data from autochecker

Examples:
- "how many students are enrolled" → get_learners()
- "which lab has the lowest pass rate" → get_pass_rates for each lab (you'll need multiple calls)
- "sync the data" → trigger_sync()
- "lab 4 pass rates" → get_pass_rates(lab="lab-04")

When user asks about lowest/highest pass rate, you may need to call get_pass_rates for multiple labs.
When user asks about student count, call get_learners() and count the results.

Answer in natural language, be concise. Include numbers from the data.

For comparison questions like "which lab has the lowest pass rate":
1. First call get_labs() to get all labs
2. Then call get_pass_rates() for each lab
3. Compare the average pass rates to find the lowest
4. Answer with the lab name and its pass rate"""

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

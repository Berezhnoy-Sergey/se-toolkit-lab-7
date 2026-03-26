"""Backend API client."""
import os
import sys 
from dotenv import load_dotenv

# Загружаем .env.bot.secret из корня проекта
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env.bot.secret'))

import httpx
from typing import List, Dict, Any

LMS_API_KEY = os.getenv("LMS_API_KEY", "")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")

# Отладка
print(f"Loaded LMS_API_KEY: {'*' * len(LMS_API_KEY) if LMS_API_KEY else 'EMPTY'}", file=sys.stderr)
print(f"Loaded LMS_API_BASE_URL: {LMS_API_BASE_URL}", file=sys.stderr)

class BackendAPI:
    def __init__(self):
        self.base_url = LMS_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {LMS_API_KEY}"}
        print(f"Headers: {self.headers}", file=sys.stderr)
    
    async def get_items(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/items/",
                headers=self.headers,
                timeout=10.0
            )
            resp.raise_for_status()
            return resp.json()
    
    async def get_pass_rates(self, lab: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/analytics/pass-rates",
                params={"lab": lab},
                headers=self.headers,
                timeout=10.0
            )
            resp.raise_for_status()
            return resp.json()
    
    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/items/",
                    headers=self.headers,
                    timeout=5.0
                )
                return resp.status_code == 200
        except Exception as e:
            print(f"Health check error: {e}", file=sys.stderr)
            return False

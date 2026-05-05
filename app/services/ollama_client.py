import json

import httpx

from app.core.settings import settings


class OllamaClient:
    def __init__(self):
        self._base_url = settings.ollama_base_url
        self._model = settings.ollama_model

    def _chat(self, prompt: str) -> str:
        response = httpx.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self._model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "stream": False,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()
        return data["message"]["content"]

    def generate_task_summary(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> str:
        description_text = description or "No description provided."

        prompt = (
            "You are a concise productivity assistant. "
            "Summarize the task clearly in one short paragraph. "
            "Do not invent information. "
            "Use only the provided task data.\n\n"
            f"Task title: {title}\n"
            f"Task description: {description_text}\n"
            f"Task status: {status}\n"
            f"Task priority: {priority}\n"
        )

        return self._chat(prompt)

    def generate_task_breakdown(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> list[dict]:
        description_text = description or "No description provided."

        prompt = (
            "You are a productivity assistant. "
            "Break the provided task into 3 to 7 actionable subtasks.\n\n"
            "Return ONLY valid JSON. "
            "Do not use markdown. "
            "Do not wrap the JSON in backticks. "
            "The JSON must be an array of objects. "
            "Each object must have exactly these fields: "
            "title, description, priority. "
            "Priority must be one of: LOW, MEDIUM, HIGH, CRITICAL.\n\n"
            f"Task title: {title}\n"
            f"Task description: {description_text}\n"
            f"Task status: {status}\n"
            f"Task priority: {priority}\n"
        )

        return self._chat(prompt)

ollama_client = OllamaClient()

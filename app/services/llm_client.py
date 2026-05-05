from abc import ABC, abstractmethod

from app.services.ollama_client import ollama_client


class LLMClient(ABC):
    @abstractmethod
    def generate_task_summary(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> str:
        pass

    @abstractmethod
    def generate_task_breakdown(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> str:
        pass


class OllamaLLMClient(LLMClient):
    def generate_task_summary(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> str:
        return ollama_client.generate_task_summary(
            title=title,
            description=description,
            status=status,
            priority=priority,
        )

    def generate_task_breakdown(
        self,
        title: str,
        description: str | None,
        status: str,
        priority: str,
    ) -> str:
        return ollama_client.generate_task_breakdown(
            title=title,
            description=description,
            status=status,
            priority=priority,
        )


llm_client: LLMClient = OllamaLLMClient()
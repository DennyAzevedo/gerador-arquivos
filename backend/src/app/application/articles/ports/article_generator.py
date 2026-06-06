from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ArticleGenerationInput:
    topic: str
    keywords: str | None = None
    tone: str | None = None


@dataclass
class GeneratedArticle:
    title: str
    content: str


class ArticleGenerator(ABC):
    """Porta para um provedor de geração de artigos (ex.: Gemini)."""

    @abstractmethod
    async def generate(self, data: ArticleGenerationInput) -> GeneratedArticle: ...

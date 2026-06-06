from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class WordPressArticlePayload:
    article_id: UUID
    title: str
    content: str
    topic: str
    keywords: str | None = None
    tone: str | None = None


@dataclass
class WordPressPublishResult:
    post_id: str
    post_url: str
    mocked: bool
    message: str


class WordPressPublisher(ABC):
    """Porta para publicação de artigos no WordPress."""

    @abstractmethod
    async def publish(self, article: WordPressArticlePayload) -> WordPressPublishResult: ...

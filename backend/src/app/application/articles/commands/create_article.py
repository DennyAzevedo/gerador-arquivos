from dataclasses import dataclass
from uuid import UUID, uuid4

from app.domain.articles.entities import Article, ArticleStatus
from app.domain.articles.repository import ArticleRepository


@dataclass
class CreateArticleInput:
    user_id: UUID
    title: str
    content: str
    topic: str
    keywords: str | None = None
    tone: str | None = None
    status: ArticleStatus = ArticleStatus.DRAFT


class CreateArticleUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, data: CreateArticleInput) -> Article:
        article = Article(
            id=uuid4(),
            title=data.title,
            content=data.content,
            topic=data.topic,
            user_id=data.user_id,
            status=data.status,
            keywords=data.keywords,
            tone=data.tone,
        )
        return await self._repository.add(article)

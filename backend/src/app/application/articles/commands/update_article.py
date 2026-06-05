from dataclasses import dataclass
from uuid import UUID

from app.domain.articles.entities import Article, ArticleStatus
from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository


@dataclass
class UpdateArticleInput:
    article_id: UUID
    user_id: UUID
    title: str | None = None
    content: str | None = None
    keywords: str | None = None
    tone: str | None = None
    status: ArticleStatus | None = None


class UpdateArticleUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, data: UpdateArticleInput) -> Article:
        article = await self._repository.get_by_id(data.article_id)
        if article is None or article.user_id != data.user_id:
            raise ArticleNotFoundError(data.article_id)

        if data.title is not None:
            article.title = data.title
        if data.content is not None:
            article.content = data.content
        if data.keywords is not None:
            article.keywords = data.keywords
        if data.tone is not None:
            article.tone = data.tone
        if data.status is not None:
            article.status = data.status

        return await self._repository.update(article)

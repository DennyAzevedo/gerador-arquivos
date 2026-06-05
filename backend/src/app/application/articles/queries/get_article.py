from uuid import UUID

from app.domain.articles.entities import Article
from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository


class GetArticleUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, article_id: UUID, user_id: UUID) -> Article:
        article = await self._repository.get_by_id(article_id)
        if article is None or article.user_id != user_id:
            raise ArticleNotFoundError(article_id)
        return article

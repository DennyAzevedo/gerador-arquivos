from uuid import UUID

from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository


class DeleteArticleUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, article_id: UUID, user_id: UUID) -> None:
        article = await self._repository.get_by_id(article_id)
        if article is None or article.user_id != user_id:
            raise ArticleNotFoundError(article_id)
        await self._repository.delete(article_id)

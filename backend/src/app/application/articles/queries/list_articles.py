from uuid import UUID

from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepository


class ListArticlesUseCase:
    def __init__(self, repository: ArticleRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: UUID) -> list[Article]:
        return await self._repository.list_by_user(user_id)

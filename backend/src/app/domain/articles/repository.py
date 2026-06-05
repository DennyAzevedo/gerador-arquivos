from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.articles.entities import Article


class ArticleRepository(ABC):
    """Contrato de persistência de artigos para a camada de aplicação."""

    @abstractmethod
    async def add(self, article: Article) -> Article: ...

    @abstractmethod
    async def get_by_id(self, article_id: UUID) -> Article | None: ...

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Article]: ...

    @abstractmethod
    async def update(self, article: Article) -> Article: ...

    @abstractmethod
    async def delete(self, article_id: UUID) -> None: ...

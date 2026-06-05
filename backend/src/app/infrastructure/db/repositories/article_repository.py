from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.articles.entities import Article
from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository
from app.infrastructure.db.mappers.article_mapper import to_domain
from app.infrastructure.db.models import ArticleModel


class SqlAlchemyArticleRepository(ArticleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, article: Article) -> Article:
        model = ArticleModel(
            id=article.id,
            title=article.title,
            content=article.content,
            topic=article.topic,
            keywords=article.keywords,
            tone=article.tone,
            status=article.status.value,
            user_id=article.user_id,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return to_domain(model)

    async def get_by_id(self, article_id: UUID) -> Article | None:
        model = await self._session.get(ArticleModel, article_id)
        return to_domain(model) if model is not None else None

    async def list_by_user(self, user_id: UUID) -> list[Article]:
        result = await self._session.execute(
            select(ArticleModel)
            .where(ArticleModel.user_id == user_id)
            .order_by(ArticleModel.created_at.desc())
        )
        return [to_domain(model) for model in result.scalars().all()]

    async def update(self, article: Article) -> Article:
        model = await self._session.get(ArticleModel, article.id)
        if model is None:
            raise ArticleNotFoundError(article.id)
        model.title = article.title
        model.content = article.content
        model.topic = article.topic
        model.keywords = article.keywords
        model.tone = article.tone
        model.status = article.status.value
        await self._session.commit()
        await self._session.refresh(model)
        return to_domain(model)

    async def delete(self, article_id: UUID) -> None:
        model = await self._session.get(ArticleModel, article_id)
        if model is None:
            raise ArticleNotFoundError(article_id)
        await self._session.delete(model)
        await self._session.commit()

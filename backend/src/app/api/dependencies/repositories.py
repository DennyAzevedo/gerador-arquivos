from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.articles.repository import ArticleRepository
from app.domain.users.repository import UserRepository
from app.infrastructure.db.repositories.article_repository import SqlAlchemyArticleRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.db.session import get_async_session


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_article_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ArticleRepository:
    return SqlAlchemyArticleRepository(session)

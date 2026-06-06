from uuid import uuid4

import pytest

from app.domain.articles.entities import Article, ArticleStatus
from app.infrastructure.db.models import UserModel
from app.infrastructure.db.repositories.article_repository import SqlAlchemyArticleRepository


async def _create_user(db_session) -> UserModel:
    user = UserModel(
        id=uuid4(),
        email=f"repo-{uuid4()}@exemplo.com",
        hashed_password="hashed-password",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user


async def test_sqlalchemy_article_repository_crud(db_session) -> None:
    user = await _create_user(db_session)
    repository = SqlAlchemyArticleRepository(db_session)
    article = Article(
        id=uuid4(),
        title="Integração",
        content="Conteúdo de teste",
        topic="pytest",
        user_id=user.id,
        status=ArticleStatus.DRAFT,
    )

    created = await repository.add(article)
    assert created.id == article.id

    fetched = await repository.get_by_id(article.id)
    assert fetched is not None
    assert fetched.title == "Integração"

    listed = await repository.list_by_user(user.id)
    assert len(listed) == 1

    fetched.title = "Atualizado"
    fetched.status = ArticleStatus.PUBLISHED
    updated = await repository.update(fetched)
    assert updated.status == ArticleStatus.PUBLISHED

    await repository.delete(article.id)
    assert await repository.get_by_id(article.id) is None


async def test_sqlalchemy_article_repository_update_missing_raises(db_session) -> None:
    user = await _create_user(db_session)
    repository = SqlAlchemyArticleRepository(db_session)
    missing = Article(
        id=uuid4(),
        title="Inexistente",
        content="Conteúdo",
        topic="pytest",
        user_id=user.id,
    )
    from app.domain.articles.exceptions import ArticleNotFoundError

    with pytest.raises(ArticleNotFoundError):
        await repository.update(missing)

from uuid import uuid4

import pytest

from app.application.articles.commands.create_article import CreateArticleInput, CreateArticleUseCase
from app.application.articles.commands.delete_article import DeleteArticleUseCase
from app.application.articles.commands.generate_article import GenerateArticleUseCase
from app.application.articles.commands.publish_article_to_wordpress import (
    PublishArticleToWordPressUseCase,
)
from app.application.articles.commands.update_article import UpdateArticleInput, UpdateArticleUseCase
from app.application.articles.exceptions import ArticleGenerationError
from app.application.articles.ports.article_generator import ArticleGenerationInput
from app.application.articles.queries.get_article import GetArticleUseCase
from app.application.articles.queries.list_articles import ListArticlesUseCase
from app.domain.articles.entities import ArticleStatus
from app.domain.articles.exceptions import ArticleNotFoundError
from tests.support.fakes import FakeArticleGenerator, FakeArticleRepository, FakeWordPressPublisher


@pytest.fixture
def repository() -> FakeArticleRepository:
    return FakeArticleRepository()


@pytest.fixture
def user_id():
    return uuid4()


async def test_create_article_persists_draft(repository: FakeArticleRepository, user_id) -> None:
    use_case = CreateArticleUseCase(repository)
    article = await use_case.execute(
        CreateArticleInput(
            user_id=user_id,
            title="Meu artigo",
            content="Conteúdo",
            topic="Tema",
        )
    )
    assert article.title == "Meu artigo"
    assert article.status == ArticleStatus.DRAFT
    assert await repository.get_by_id(article.id) is not None


async def test_update_article_changes_fields(repository: FakeArticleRepository, user_id) -> None:
    create = CreateArticleUseCase(repository)
    created = await create.execute(
        CreateArticleInput(
            user_id=user_id,
            title="Original",
            content="Conteúdo",
            topic="Tema",
        )
    )
    update = UpdateArticleUseCase(repository)
    updated = await update.execute(
        UpdateArticleInput(
            article_id=created.id,
            user_id=user_id,
            title="Atualizado",
            status=ArticleStatus.PUBLISHED,
        )
    )
    assert updated.title == "Atualizado"
    assert updated.status == ArticleStatus.PUBLISHED


async def test_update_article_raises_when_not_owner(repository: FakeArticleRepository, user_id) -> None:
    create = CreateArticleUseCase(repository)
    created = await create.execute(
        CreateArticleInput(
            user_id=user_id,
            title="Original",
            content="Conteúdo",
            topic="Tema",
        )
    )
    update = UpdateArticleUseCase(repository)
    with pytest.raises(ArticleNotFoundError):
        await update.execute(
            UpdateArticleInput(
                article_id=created.id,
                user_id=uuid4(),
                title="Tentativa",
            )
        )


async def test_delete_article_removes_entry(repository: FakeArticleRepository, user_id) -> None:
    create = CreateArticleUseCase(repository)
    created = await create.execute(
        CreateArticleInput(
            user_id=user_id,
            title="Excluir",
            content="Conteúdo",
            topic="Tema",
        )
    )
    delete = DeleteArticleUseCase(repository)
    await delete.execute(created.id, user_id)
    assert await repository.get_by_id(created.id) is None


async def test_get_and_list_filter_by_user(repository: FakeArticleRepository, user_id) -> None:
    create = CreateArticleUseCase(repository)
    await create.execute(
        CreateArticleInput(
            user_id=user_id,
            title="Artigo 1",
            content="Conteúdo",
            topic="Tema",
        )
    )
    other_user = uuid4()
    await create.execute(
        CreateArticleInput(
            user_id=other_user,
            title="Artigo 2",
            content="Conteúdo",
            topic="Tema",
        )
    )
    listed = await ListArticlesUseCase(repository).execute(user_id)
    assert len(listed) == 1
    assert listed[0].title == "Artigo 1"
    assert await GetArticleUseCase(repository).execute(listed[0].id, user_id)


async def test_generate_article_delegates_to_generator() -> None:
    generator = FakeArticleGenerator()
    use_case = GenerateArticleUseCase(generator)
    result = await use_case.execute(ArticleGenerationInput(topic="Python"))
    assert result.title == "Título gerado"
    assert generator.last_input is not None
    assert generator.last_input.topic == "Python"


async def test_generate_article_propagates_errors() -> None:
    generator = FakeArticleGenerator(error=ArticleGenerationError("Falha"))
    use_case = GenerateArticleUseCase(generator)
    with pytest.raises(ArticleGenerationError):
        await use_case.execute(ArticleGenerationInput(topic="Python"))


async def test_publish_to_wordpress_updates_status(
    repository: FakeArticleRepository,
    user_id,
) -> None:
    created = await CreateArticleUseCase(repository).execute(
        CreateArticleInput(
            user_id=user_id,
            title="Para WP",
            content="Conteúdo",
            topic="Tema",
        )
    )
    publisher = FakeWordPressPublisher()
    use_case = PublishArticleToWordPressUseCase(repository, publisher)

    result = await use_case.execute(created.id, user_id)

    assert result.mocked is True
    assert publisher.last_payload is not None
    assert publisher.last_payload.title == "Para WP"
    updated = await repository.get_by_id(created.id)
    assert updated is not None
    assert updated.status == ArticleStatus.PUBLISHED

from uuid import uuid4

from app.domain.articles.entities import Article, ArticleStatus
from app.domain.articles.exceptions import ArticleNotFoundError


def test_article_status_values() -> None:
    assert ArticleStatus.DRAFT.value == "draft"
    assert ArticleStatus.PUBLISHED.value == "published"


def test_article_entity_defaults_to_draft() -> None:
    article = Article(
        id=uuid4(),
        title="Título",
        content="Conteúdo",
        topic="Tema",
        user_id=uuid4(),
    )
    assert article.status == ArticleStatus.DRAFT


def test_article_not_found_error_exposes_id() -> None:
    article_id = uuid4()
    error = ArticleNotFoundError(article_id)
    assert error.article_id == article_id
    assert str(article_id) in str(error)

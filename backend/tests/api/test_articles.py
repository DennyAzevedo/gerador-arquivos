from app.api.dependencies.services import get_article_generator
from app.application.articles.exceptions import ArticleGenerationError
from app.application.articles.ports.article_generator import GeneratedArticle
from app.main import app
from tests.support.fakes import FakeArticleGenerator


async def test_articles_crud_flow(client, auth_headers) -> None:
    create = await client.post(
        "/articles",
        headers=auth_headers,
        json={
            "title": "API Artigo",
            "content": "Conteúdo",
            "topic": "integração",
            "status": "draft",
        },
    )
    assert create.status_code == 201
    article_id = create.json()["id"]

    listing = await client.get("/articles", headers=auth_headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    detail = await client.get(f"/articles/{article_id}", headers=auth_headers)
    assert detail.status_code == 200

    update = await client.put(
        f"/articles/{article_id}",
        headers=auth_headers,
        json={"title": "API Atualizado", "status": "published"},
    )
    assert update.status_code == 200
    assert update.json()["status"] == "published"

    delete = await client.delete(f"/articles/{article_id}", headers=auth_headers)
    assert delete.status_code == 204

    missing = await client.get(f"/articles/{article_id}", headers=auth_headers)
    assert missing.status_code == 404


async def test_articles_require_authentication(client) -> None:
    response = await client.get("/articles")
    assert response.status_code == 401


async def test_generate_article_success_with_override(client, auth_headers) -> None:
    app.dependency_overrides[get_article_generator] = lambda: FakeArticleGenerator(
        result=GeneratedArticle(title="Gerado", content="Texto")
    )
    try:
        response = await client.post(
            "/articles/generate",
            headers=auth_headers,
            json={"topic": "inteligência artificial"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Gerado"
    finally:
        app.dependency_overrides.pop(get_article_generator, None)


async def test_generate_article_failure_returns_502(client, auth_headers) -> None:
    app.dependency_overrides[get_article_generator] = lambda: FakeArticleGenerator(
        error=ArticleGenerationError("Falha ao gerar")
    )
    try:
        response = await client.post(
            "/articles/generate",
            headers=auth_headers,
            json={"topic": "inteligência artificial"},
        )
        assert response.status_code == 502
    finally:
        app.dependency_overrides.pop(get_article_generator, None)

from app.api.dependencies.services import get_article_generator, get_wordpress_publisher
from app.application.articles.exceptions import ArticleGenerationError, WordPressPublishError
from app.application.articles.ports.article_generator import GeneratedArticle
from app.main import app
from tests.support.fakes import FakeArticleGenerator, FakeWordPressPublisher


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


async def test_update_article_rejects_empty_title(client, auth_headers) -> None:
    create = await client.post(
        "/articles",
        headers=auth_headers,
        json={
            "title": "Artigo válido",
            "content": "Conteúdo",
            "topic": "validação",
            "status": "draft",
        },
    )
    article_id = create.json()["id"]

    response = await client.put(
        f"/articles/{article_id}",
        headers=auth_headers,
        json={"title": ""},
    )
    assert response.status_code == 422


async def test_update_article_rejects_empty_content(client, auth_headers) -> None:
    create = await client.post(
        "/articles",
        headers=auth_headers,
        json={
            "title": "Artigo válido",
            "content": "Conteúdo",
            "topic": "validação",
            "status": "draft",
        },
    )
    article_id = create.json()["id"]

    response = await client.put(
        f"/articles/{article_id}",
        headers=auth_headers,
        json={"content": ""},
    )
    assert response.status_code == 422


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


async def test_publish_wordpress_success_with_mock(client, auth_headers) -> None:
    create = await client.post(
        "/articles",
        headers=auth_headers,
        json={
            "title": "Artigo WP",
            "content": "Conteúdo",
            "topic": "wordpress",
            "status": "draft",
        },
    )
    article_id = create.json()["id"]

    app.dependency_overrides[get_wordpress_publisher] = lambda: FakeWordPressPublisher()
    try:
        response = await client.post(
            f"/articles/{article_id}/publish-wordpress",
            headers=auth_headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert body["mocked"] is True
        assert "simulado" in body["message"].lower()

        detail = await client.get(f"/articles/{article_id}", headers=auth_headers)
        assert detail.json()["status"] == "published"
    finally:
        app.dependency_overrides.pop(get_wordpress_publisher, None)


async def test_publish_wordpress_not_found(client, auth_headers) -> None:
    app.dependency_overrides[get_wordpress_publisher] = lambda: FakeWordPressPublisher()
    try:
        response = await client.post(
            "/articles/00000000-0000-0000-0000-000000000099/publish-wordpress",
            headers=auth_headers,
        )
        assert response.status_code == 404
    finally:
        app.dependency_overrides.pop(get_wordpress_publisher, None)


async def test_publish_wordpress_failure_returns_502(client, auth_headers) -> None:
    create = await client.post(
        "/articles",
        headers=auth_headers,
        json={
            "title": "Artigo WP",
            "content": "Conteúdo",
            "topic": "wordpress",
            "status": "draft",
        },
    )
    article_id = create.json()["id"]

    app.dependency_overrides[get_wordpress_publisher] = lambda: FakeWordPressPublisher(
        error=WordPressPublishError("Falha ao publicar")
    )
    try:
        response = await client.post(
            f"/articles/{article_id}/publish-wordpress",
            headers=auth_headers,
        )
        assert response.status_code == 502
    finally:
        app.dependency_overrides.pop(get_wordpress_publisher, None)

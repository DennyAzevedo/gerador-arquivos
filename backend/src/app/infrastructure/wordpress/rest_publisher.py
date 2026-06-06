import base64
import logging

import httpx

from app.application.articles.exceptions import WordPressPublishError
from app.application.articles.ports.wordpress_publisher import (
    WordPressArticlePayload,
    WordPressPublisher,
    WordPressPublishResult,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class RestWordPressPublisher(WordPressPublisher):
    """Publica artigos via WordPress REST API (/wp-json/wp/v2/posts)."""

    def __init__(self) -> None:
        if not settings.wordpress_url:
            raise WordPressPublishError("WORDPRESS_URL não configurada.")
        if not settings.wordpress_username or not settings.wordpress_app_password:
            raise WordPressPublishError(
                "WORDPRESS_USERNAME e WORDPRESS_APP_PASSWORD são obrigatórios para publicação real."
            )

        self._base_url = settings.wordpress_url.rstrip("/")
        credentials = f"{settings.wordpress_username}:{settings.wordpress_app_password}"
        token = base64.b64encode(credentials.encode()).decode()
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    async def publish(self, article: WordPressArticlePayload) -> WordPressPublishResult:
        payload = {
            "title": article.title,
            "content": article.content,
            "status": "publish",
            "excerpt": article.topic,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._base_url}/wp-json/wp/v2/posts",
                    headers=self._headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            logger.exception("WordPress REST API request failed")
            raise WordPressPublishError("Falha ao publicar no WordPress.") from exc

        post_id = str(data.get("id", ""))
        post_url = str(data.get("link", self._base_url))

        return WordPressPublishResult(
            post_id=post_id,
            post_url=post_url,
            mocked=False,
            message="Artigo publicado no WordPress com sucesso.",
        )

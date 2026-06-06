from app.application.articles.ports.wordpress_publisher import (
    WordPressArticlePayload,
    WordPressPublisher,
    WordPressPublishResult,
)
from app.core.config import settings


class MockWordPressPublisher(WordPressPublisher):
    """Simula envio ao WordPress até a integração real ser habilitada."""

    async def publish(self, article: WordPressArticlePayload) -> WordPressPublishResult:
        base_url = settings.wordpress_url.rstrip("/") or "https://seu-blog.wordpress.com"
        post_id = f"mock-{article.article_id}"
        post_url = f"{base_url}/?p={post_id}"

        return WordPressPublishResult(
            post_id=post_id,
            post_url=post_url,
            mocked=True,
            message=(
                "Artigo enviado ao WordPress (simulado). "
                "Defina WORDPRESS_MOCK=false e configure as credenciais para publicação real."
            ),
        )

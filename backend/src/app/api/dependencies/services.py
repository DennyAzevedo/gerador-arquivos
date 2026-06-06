from app.application.articles.ports.article_generator import ArticleGenerator
from app.application.articles.ports.wordpress_publisher import WordPressPublisher
from app.core.config import settings
from app.infrastructure.gemini.article_generator import GeminiArticleGenerator
from app.infrastructure.wordpress.mock_publisher import MockWordPressPublisher
from app.infrastructure.wordpress.rest_publisher import RestWordPressPublisher


def get_article_generator() -> ArticleGenerator:
    return GeminiArticleGenerator()


def get_wordpress_publisher() -> WordPressPublisher:
    if settings.wordpress_mock:
        return MockWordPressPublisher()
    return RestWordPressPublisher()

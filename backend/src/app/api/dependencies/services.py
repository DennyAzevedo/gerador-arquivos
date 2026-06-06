from app.application.articles.ports.article_generator import ArticleGenerator
from app.infrastructure.gemini.article_generator import GeminiArticleGenerator


def get_article_generator() -> ArticleGenerator:
    return GeminiArticleGenerator()

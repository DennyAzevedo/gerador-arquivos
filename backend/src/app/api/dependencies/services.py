from app.application.articles.ports.article_generator import ArticleGenerator
from app.infrastructure.openai.article_generator import OpenAIArticleGenerator


def get_article_generator() -> ArticleGenerator:
    return OpenAIArticleGenerator()

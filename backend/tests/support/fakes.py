from uuid import UUID

from app.application.articles.ports.article_generator import (
    ArticleGenerationInput,
    ArticleGenerator,
    GeneratedArticle,
)
from app.application.articles.ports.wordpress_publisher import (
    WordPressArticlePayload,
    WordPressPublisher,
    WordPressPublishResult,
)
from app.domain.articles.entities import Article
from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository


class FakeArticleRepository(ArticleRepository):
    def __init__(self) -> None:
        self._articles: dict[UUID, Article] = {}

    async def add(self, article: Article) -> Article:
        self._articles[article.id] = article
        return article

    async def get_by_id(self, article_id: UUID) -> Article | None:
        return self._articles.get(article_id)

    async def list_by_user(self, user_id: UUID) -> list[Article]:
        return [article for article in self._articles.values() if article.user_id == user_id]

    async def update(self, article: Article) -> Article:
        if article.id not in self._articles:
            raise ArticleNotFoundError(article.id)
        self._articles[article.id] = article
        return article

    async def delete(self, article_id: UUID) -> None:
        if article_id not in self._articles:
            raise ArticleNotFoundError(article_id)
        del self._articles[article_id]


class FakeArticleGenerator(ArticleGenerator):
    def __init__(self, result: GeneratedArticle | None = None, error: Exception | None = None) -> None:
        self._result = result or GeneratedArticle(title="Título gerado", content="Conteúdo gerado")
        self._error = error
        self.last_input: ArticleGenerationInput | None = None

    async def generate(self, data: ArticleGenerationInput) -> GeneratedArticle:
        self.last_input = data
        if self._error:
            raise self._error
        return self._result


class FakeWordPressPublisher(WordPressPublisher):
    def __init__(self, result: WordPressPublishResult | None = None, error: Exception | None = None) -> None:
        self._result = result or WordPressPublishResult(
            post_id="mock-123",
            post_url="https://exemplo.wordpress.com/?p=mock-123",
            mocked=True,
            message="Artigo enviado ao WordPress (simulado).",
        )
        self._error = error
        self.last_payload: WordPressArticlePayload | None = None

    async def publish(self, article: WordPressArticlePayload) -> WordPressPublishResult:
        self.last_payload = article
        if self._error:
            raise self._error
        return self._result

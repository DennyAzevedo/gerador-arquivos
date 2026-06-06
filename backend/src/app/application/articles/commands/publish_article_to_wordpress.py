from uuid import UUID

from app.application.articles.ports.wordpress_publisher import (
    WordPressArticlePayload,
    WordPressPublisher,
    WordPressPublishResult,
)
from app.domain.articles.entities import ArticleStatus
from app.domain.articles.exceptions import ArticleNotFoundError
from app.domain.articles.repository import ArticleRepository


class PublishArticleToWordPressUseCase:
    def __init__(
        self,
        repository: ArticleRepository,
        publisher: WordPressPublisher,
    ) -> None:
        self._repository = repository
        self._publisher = publisher

    async def execute(self, article_id: UUID, user_id: UUID) -> WordPressPublishResult:
        article = await self._repository.get_by_id(article_id)
        if article is None or article.user_id != user_id:
            raise ArticleNotFoundError(article_id)

        result = await self._publisher.publish(
            WordPressArticlePayload(
                article_id=article.id,
                title=article.title,
                content=article.content,
                topic=article.topic,
                keywords=article.keywords,
                tone=article.tone,
            )
        )

        if article.status != ArticleStatus.PUBLISHED:
            article.status = ArticleStatus.PUBLISHED
            await self._repository.update(article)

        return result

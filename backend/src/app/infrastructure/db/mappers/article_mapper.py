from app.domain.articles.entities import Article, ArticleStatus
from app.infrastructure.db.models import ArticleModel


def to_domain(model: ArticleModel) -> Article:
    return Article(
        id=model.id,
        title=model.title,
        content=model.content,
        topic=model.topic,
        user_id=model.user_id,
        status=ArticleStatus(model.status),
        keywords=model.keywords,
        tone=model.tone,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )

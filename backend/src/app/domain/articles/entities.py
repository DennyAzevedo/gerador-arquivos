from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class ArticleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


@dataclass
class Article:
    """Entidade de domínio do artigo, independente de framework ou ORM."""

    id: UUID
    title: str
    content: str
    topic: str
    user_id: UUID
    status: ArticleStatus = ArticleStatus.DRAFT
    keywords: str | None = None
    tone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

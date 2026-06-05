import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.articles.entities import ArticleStatus


class GenerateArticleRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    keywords: str | None = Field(default=None, max_length=500)
    tone: str | None = Field(default=None, max_length=100)


class GeneratedArticleResponse(BaseModel):
    title: str
    content: str


class ArticleCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    topic: str = Field(min_length=1, max_length=500)
    keywords: str | None = Field(default=None, max_length=500)
    tone: str | None = Field(default=None, max_length=100)
    status: ArticleStatus = ArticleStatus.DRAFT


class ArticleUpdateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = None
    keywords: str | None = Field(default=None, max_length=500)
    tone: str | None = Field(default=None, max_length=100)
    status: ArticleStatus | None = None


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    topic: str
    keywords: str | None
    tone: str | None
    status: ArticleStatus
    created_at: datetime
    updated_at: datetime

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.repositories import get_article_repository
from app.api.dependencies.services import get_article_generator
from app.api.schemas.article import (
    ArticleCreateRequest,
    ArticleResponse,
    ArticleUpdateRequest,
    GenerateArticleRequest,
    GeneratedArticleResponse,
)
from app.application.articles.commands.create_article import (
    CreateArticleInput,
    CreateArticleUseCase,
)
from app.application.articles.commands.delete_article import DeleteArticleUseCase
from app.application.articles.commands.generate_article import GenerateArticleUseCase
from app.application.articles.commands.update_article import (
    UpdateArticleInput,
    UpdateArticleUseCase,
)
from app.application.articles.exceptions import ArticleGenerationError
from app.application.articles.ports.article_generator import (
    ArticleGenerationInput,
    ArticleGenerator,
)
from app.application.articles.queries.get_article import GetArticleUseCase
from app.application.articles.queries.list_articles import ListArticlesUseCase
from app.domain.articles.repository import ArticleRepository
from app.infrastructure.auth import current_active_user
from app.infrastructure.db.models import UserModel

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/generate", response_model=GeneratedArticleResponse)
async def generate_article(
    payload: GenerateArticleRequest,
    user: UserModel = Depends(current_active_user),
    generator: ArticleGenerator = Depends(get_article_generator),
) -> GeneratedArticleResponse:
    use_case = GenerateArticleUseCase(generator)
    try:
        result = await use_case.execute(
            ArticleGenerationInput(
                topic=payload.topic,
                keywords=payload.keywords,
                tone=payload.tone,
            )
        )
    except ArticleGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    return GeneratedArticleResponse(title=result.title, content=result.content)


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: ArticleCreateRequest,
    user: UserModel = Depends(current_active_user),
    repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleResponse:
    use_case = CreateArticleUseCase(repository)
    article = await use_case.execute(
        CreateArticleInput(
            user_id=user.id,
            title=payload.title,
            content=payload.content,
            topic=payload.topic,
            keywords=payload.keywords,
            tone=payload.tone,
            status=payload.status,
        )
    )
    return ArticleResponse.model_validate(article)


@router.get("", response_model=list[ArticleResponse])
async def list_articles(
    user: UserModel = Depends(current_active_user),
    repository: ArticleRepository = Depends(get_article_repository),
) -> list[ArticleResponse]:
    use_case = ListArticlesUseCase(repository)
    articles = await use_case.execute(user.id)
    return [ArticleResponse.model_validate(article) for article in articles]


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: UUID,
    user: UserModel = Depends(current_active_user),
    repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleResponse:
    use_case = GetArticleUseCase(repository)
    article = await use_case.execute(article_id, user.id)
    return ArticleResponse.model_validate(article)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: UUID,
    payload: ArticleUpdateRequest,
    user: UserModel = Depends(current_active_user),
    repository: ArticleRepository = Depends(get_article_repository),
) -> ArticleResponse:
    use_case = UpdateArticleUseCase(repository)
    article = await use_case.execute(
        UpdateArticleInput(
            article_id=article_id,
            user_id=user.id,
            title=payload.title,
            content=payload.content,
            keywords=payload.keywords,
            tone=payload.tone,
            status=payload.status,
        )
    )
    return ArticleResponse.model_validate(article)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: UUID,
    user: UserModel = Depends(current_active_user),
    repository: ArticleRepository = Depends(get_article_repository),
) -> None:
    use_case = DeleteArticleUseCase(repository)
    await use_case.execute(article_id, user.id)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import articles, health
from app.api.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.config import settings
from app.domain.articles.exceptions import ArticleNotFoundError
from app.infrastructure.auth import auth_backend, fastapi_users


async def article_not_found_handler(
    request: Request,
    exc: ArticleNotFoundError,
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Artigo não encontrado"})


def create_app() -> FastAPI:
    app = FastAPI(title="Gerador de Artigos para WordPress", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(ArticleNotFoundError, article_not_found_handler)

    app.include_router(health.router)
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
    app.include_router(articles.router)

    return app


app = create_app()

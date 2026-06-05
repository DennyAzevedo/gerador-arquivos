from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.core.config import settings

JWT_LIFETIME_SECONDS = 3600

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.jwt_secret, lifetime_seconds=JWT_LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

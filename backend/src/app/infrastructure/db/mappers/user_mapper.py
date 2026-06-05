from app.domain.users.entities import User
from app.infrastructure.db.models import UserModel


def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        is_active=model.is_active,
        is_superuser=model.is_superuser,
        is_verified=model.is_verified,
        created_at=model.created_at,
    )

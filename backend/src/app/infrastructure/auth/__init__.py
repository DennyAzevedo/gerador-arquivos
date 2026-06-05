import uuid

from fastapi_users import FastAPIUsers

from app.infrastructure.auth.auth_backend import auth_backend
from app.infrastructure.auth.user_manager import get_user_manager
from app.infrastructure.db.models import UserModel

fastapi_users = FastAPIUsers[UserModel, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

__all__ = ["auth_backend", "current_active_user", "fastapi_users"]

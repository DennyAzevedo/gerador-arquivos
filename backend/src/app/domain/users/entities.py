from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    """Entidade de domínio do usuário, independente de framework ou ORM."""

    id: UUID
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime | None = None

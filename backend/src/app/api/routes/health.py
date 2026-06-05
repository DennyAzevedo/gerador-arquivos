import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_async_session

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness: indica que o serviço está no ar."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    """Readiness: verifica a conectividade com o banco de dados."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Readiness check failed: database is unavailable")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unavailable", "database": "disconnected"},
        )
    return JSONResponse(content={"status": "ready", "database": "connected"})

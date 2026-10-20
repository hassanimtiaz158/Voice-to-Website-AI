import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Message


async def create_message(
    db: AsyncSession,
    project_id: uuid.UUID,
    role: str,
    content: str,
    kind: str = "chat",
    audio_s3_key: Optional[str] = None,
) -> Message:
    """Create and persist a project chat or status message."""
    message = Message(
        project_id=project_id,
        role=role,
        content=content,
        kind=kind,
        audio_s3_key=audio_s3_key,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_messages_by_project(
    db: AsyncSession,
    project_id: uuid.UUID,
    limit: int = 100,
) -> List[Message]:
    """Retrieve chronological messages for a project."""
    stmt = (
        select(Message)
        .where(Message.project_id == project_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())

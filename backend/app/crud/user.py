import uuid
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    """Retrieve a user by their primary UUID."""
    return await db.get(User, user_id)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Retrieve a user by their lowercase email address."""
    stmt = select(User).where(User.email == email.strip().lower())
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str,
    phone: Optional[str] = None,
    role: str = "user",
) -> User:
    """Create and persist a new user record with hashed password."""
    user = User(
        email=email.strip().lower(),
        hashed_password=pwd_context.hash(password),
        full_name=full_name.strip(),
        phone=phone.strip() if phone else None,
        role=role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
    """Verify credentials and return user if valid and active."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user

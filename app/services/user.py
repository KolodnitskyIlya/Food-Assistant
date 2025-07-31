from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
        hashed_pw = get_password_hash(user_create.password)
        user = User(username=user_create.username, hashed_password=hashed_pw)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()
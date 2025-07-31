from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.services.user import UserService
from app.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await UserService.create_user(db, user_create)
        return user
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Выводим полный трейсбек в консоль
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))


@router.post("/login", response_model=Token)
async def login(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_by_username(db, user_create.username)
    if not user or not verify_password(user_create.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id)
    return Token(access_token=token)
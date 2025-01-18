from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_users, get_user_by_id
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_new_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    return await create_user(session, user)

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await get_users(session, skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
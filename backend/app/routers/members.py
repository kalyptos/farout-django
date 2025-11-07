from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..db import SessionLocal
from ..models.member_models import Member
from ..models.auth_models import User
from ..schemas.auth_schemas import MemberResponse, MemberUpdate
from ..auth import get_current_user

router = APIRouter(prefix="/members", tags=["members"])

async def get_app_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=List[MemberResponse])
async def list_members(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db)
):
    """List all members (authenticated users only)"""
    result = await db.execute(select(Member).order_by(Member.created_at.desc()))
    members = result.scalars().all()
    return members

@router.get("/{discord_id}", response_model=MemberResponse)
async def get_member(
    discord_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db)
):
    """Get member profile (authenticated users only)"""
    result = await db.execute(select(Member).where(Member.discord_id == discord_id))
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member

@router.put("/{discord_id}", response_model=MemberResponse)
async def update_member(
    discord_id: str,
    member_update: MemberUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_app_db)
):
    """Update member profile (own profile or admin)"""

    # Check if user is updating their own profile or is admin
    if current_user.discord_id != discord_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own profile"
        )

    result = await db.execute(select(Member).where(Member.discord_id == discord_id))
    member = result.scalar_one_or_none()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Update fields
    if member_update.display_name is not None:
        member.display_name = member_update.display_name
    if member_update.bio is not None:
        member.bio = member_update.bio
    if member_update.avatar_url is not None:
        member.avatar_url = member_update.avatar_url

    await db.commit()
    await db.refresh(member)

    return member

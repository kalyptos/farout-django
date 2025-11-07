from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
import math

from ..database.auth_db import get_auth_db
from ..db import SessionLocal as AppSessionLocal
from ..models.auth_models import User
from ..models.member_models import Member
from ..schemas.auth_schemas import (
    UserResponse,
    UserRoleUpdate,
    UserRankUpdate,
    UserListResponse
)
from ..auth import require_admin

router = APIRouter(prefix="/admin/users", tags=["admin-users"])

@router.get("", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    role: Optional[str] = Query(None, pattern="^(member|admin)$", description="Filter by role"),
    search: Optional[str] = Query(None, description="Search username, email, or discord_id"),
    admin_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_auth_db)
):
    """
    List all users with pagination, filtering, and search (admin only).

    Query Parameters:
    - page: Page number (default: 1)
    - limit: Users per page (default: 20, max: 100)
    - role: Filter by role ('member' or 'admin')
    - search: Search in username, email, or discord_id
    """
    # Calculate offset
    offset = (page - 1) * limit

    # Build base query
    query = select(User)
    count_query = select(func.count()).select_from(User)

    # Apply filters
    conditions = []

    if role:
        conditions.append(User.role == role)

    if search:
        search_term = f"%{search}%"
        conditions.append(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
                User.discord_id.ilike(search_term)
            )
        )

    # Apply conditions to queries
    if conditions:
        from sqlalchemy import and_
        filter_condition = and_(*conditions)
        query = query.where(filter_condition)
        count_query = count_query.where(filter_condition)

    # Order and paginate
    query = query.order_by(User.created_at.desc()).offset(offset).limit(limit)

    # Execute queries
    result = await db.execute(query)
    users = result.scalars().all()

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Calculate total pages
    pages = math.ceil(total / limit) if total > 0 else 1

    return UserListResponse(
        users=users,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )

@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    admin_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_auth_db)
):
    """
    Change user role (admin only).

    Validation:
    - Role must be 'member' or 'admin'
    - Cannot change your own role (prevent self-demotion)
    - User must exist and be active
    """
    # Prevent self-demotion
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change your own role"
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify inactive user"
        )

    user.role = role_update.role
    await db.commit()
    await db.refresh(user)

    return user

@router.put("/{user_id}/rank", response_model=UserResponse)
async def update_user_rank(
    user_id: int,
    rank_update: UserRankUpdate,
    admin_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_auth_db)
):
    """
    Change user rank and rank_image (admin only).

    Updates both the auth user's rank_image and the member's rank.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify inactive user"
        )

    # Update rank_image in auth user
    user.rank_image = rank_update.rank_image
    await db.commit()
    await db.refresh(user)

    # Also update rank in member profile if exists
    if user.discord_id:
        async with AppSessionLocal() as app_db:
            member_result = await app_db.execute(
                select(Member).where(Member.discord_id == user.discord_id)
            )
            member = member_result.scalar_one_or_none()

            if member:
                member.rank = rank_update.rank
                await app_db.commit()

    return user

@router.delete("/{user_id}")
async def deactivate_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_auth_db)
):
    """
    Soft delete user (admin only).

    Sets is_active = false for the user. Does NOT hard delete.
    Cannot delete your own account.
    """
    # Prevent self-deletion
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete your own account"
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Soft delete user
    user.is_active = False
    await db.commit()

    # Note: We do NOT soft delete the member record as Member model
    # doesn't have an is_active field. The user record being inactive
    # is sufficient to prevent access.

    return {
        "success": True,
        "message": f"User {user.username} deactivated successfully",
        "deleted_user_id": user_id
    }

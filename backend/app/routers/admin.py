from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from slugify import slugify
from ..db import SessionLocal
from ..models import BlogPost, User
from ..schemas import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogPostListResponse
)
from ..auth import get_current_admin_user
import math
from datetime import datetime

router = APIRouter(prefix="/api/admin/blog", tags=["admin-blog"])


async def get_db():
    async with SessionLocal() as session:
        yield session


def generate_unique_slug(heading: str, existing_slugs: list[str] = []) -> str:
    """Generate a unique slug from heading."""
    base_slug = slugify(heading, max_length=250)

    # If no conflicts, return base slug
    if base_slug not in existing_slugs:
        return base_slug

    # Add number suffix if slug exists
    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        if new_slug not in existing_slugs:
            return new_slug
        counter += 1


@router.get("", response_model=BlogPostListResponse)
async def list_all_blog_posts(
    page: int = 1,
    limit: int = 10,
    sort: str = "newest",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get ALL blog posts (published and unpublished) for admin interface.

    Args:
        page: Page number (default: 1)
        limit: Posts per page (default: 10, max: 50)
        sort: Sort order - 'newest' or 'oldest' (default: newest)
    """
    # Validate pagination params
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    if limit > 50:
        limit = 50

    # Calculate offset
    offset = (page - 1) * limit

    # Determine sort order
    order_by = BlogPost.created_at.desc() if sort == "newest" else BlogPost.created_at.asc()

    # Query ALL posts (no published filter)
    query = (
        select(BlogPost)
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)
    posts = result.scalars().all()

    # Get total count
    count_query = select(func.count()).select_from(BlogPost)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    total_pages = math.ceil(total / limit) if total > 0 else 1

    return BlogPostListResponse(
        posts=posts,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages
    )


@router.post("", response_model=BlogPostResponse, status_code=201)
async def create_blog_post(
    payload: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new blog post.
    Automatically generates slug from heading.
    """
    # Get existing slugs to ensure uniqueness
    existing_slugs_query = select(BlogPost.slug)
    result = await db.execute(existing_slugs_query)
    existing_slugs = [slug for (slug,) in result.all()]

    # Generate unique slug
    slug = generate_unique_slug(payload.heading, existing_slugs)

    # Create new blog post
    new_post = BlogPost(
        heading=payload.heading,
        content=payload.content,
        author=payload.author,
        feature_image=payload.feature_image,
        published=payload.published,
        slug=slug
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.get("/{post_id}", response_model=BlogPostResponse)
async def get_blog_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get a single blog post by ID (for admin editing).
    Returns both published and unpublished posts.
    """
    query = select(BlogPost).where(BlogPost.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Blog post with ID {post_id} not found"
        )

    return post


@router.put("/{post_id}", response_model=BlogPostResponse)
async def update_blog_post(
    post_id: int,
    payload: BlogPostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update an existing blog post.
    Updates slug if heading changes.
    """
    # Get existing post
    query = select(BlogPost).where(BlogPost.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Blog post with ID {post_id} not found"
        )

    # Update fields if provided
    update_data = payload.model_dump(exclude_unset=True)

    # If heading changes, regenerate slug
    if "heading" in update_data and update_data["heading"] != post.heading:
        # Get existing slugs (excluding current post's slug)
        existing_slugs_query = select(BlogPost.slug).where(BlogPost.id != post_id)
        slug_result = await db.execute(existing_slugs_query)
        existing_slugs = [slug for (slug,) in slug_result.all()]

        # Generate new unique slug
        new_slug = generate_unique_slug(update_data["heading"], existing_slugs)
        update_data["slug"] = new_slug

    # Apply updates
    for field, value in update_data.items():
        setattr(post, field, value)

    # Manually update updated_at timestamp
    post.updated_at = datetime.now()

    await db.commit()
    await db.refresh(post)

    return post


@router.delete("/{post_id}", status_code=200)
async def delete_blog_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a blog post (hard delete).
    """
    # Get existing post
    query = select(BlogPost).where(BlogPost.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Blog post with ID {post_id} not found"
        )

    await db.delete(post)
    await db.commit()

    return {
        "success": True,
        "message": f"Blog post '{post.heading}' deleted successfully",
        "deleted_id": post_id
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..db import SessionLocal
from ..models import BlogPost
from ..schemas import BlogPostResponse, BlogPostListResponse
from typing import Optional
import math

router = APIRouter(prefix="/api/blog", tags=["blog"])


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("", response_model=BlogPostListResponse)
async def list_blog_posts(
    page: int = 1,
    limit: int = 10,
    sort: str = "newest",
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of published blog posts.

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

    # Query for published posts only
    query = (
        select(BlogPost)
        .where(BlogPost.published == True)
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)
    posts = result.scalars().all()

    # Get total count for pagination
    count_query = select(func.count()).select_from(BlogPost).where(BlogPost.published == True)
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


@router.get("/{slug}", response_model=BlogPostResponse)
async def get_blog_post(slug: str, db: AsyncSession = Depends(get_db)):
    """
    Get a single blog post by its slug.
    Only returns published posts.
    """
    query = select(BlogPost).where(
        BlogPost.slug == slug,
        BlogPost.published == True
    )
    result = await db.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Blog post with slug '{slug}' not found"
        )

    return post

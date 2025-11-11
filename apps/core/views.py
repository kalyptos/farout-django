"""
Core views for Farout application.
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.members.models import Member
from apps.blog.models import BlogPost
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def health_check(request: HttpRequest) -> JsonResponse:
    """Health check endpoint for Docker and monitoring.

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: Health status information
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'farout-django',
        'version': '1.0.0'
    })


def home(request: HttpRequest) -> HttpResponse:
    """Home/landing page with recent blog posts.

    Args:
        request: HTTP request object

    Returns:
        HttpResponse: Rendered home page
    """
    # OPTIMIZATION: Use select_related to avoid N+1 queries when accessing post.author
    recent_posts = BlogPost.objects.filter(
        published=True
    ).select_related('author').order_by('-created_at')[:3]

    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Main dashboard for authenticated users.

    Args:
        request: HTTP request object (must be authenticated)

    Returns:
        HttpResponse: Rendered dashboard page
    """
    # Get organization stats
    total_members = Member.objects.count()

    # OPTIMIZATION: Only fetch needed fields for recent members
    recent_members = Member.objects.only(
        'discord_id', 'display_name', 'avatar_url', 'rank', 'created_at'
    ).order_by('-created_at')[:5]

    # OPTIMIZATION: Use select_related to avoid N+1 queries
    recent_posts = BlogPost.objects.filter(
        published=True
    ).select_related('author').order_by('-created_at')[:5]

    # Get user-specific data with proper error handling
    member: Optional[Member] = None
    if request.user.discord_id:
        try:
            member = Member.objects.get(discord_id=request.user.discord_id)
        except Member.DoesNotExist:
            logger.debug(f"No Member record found for user {request.user.id} with discord_id {request.user.discord_id}")
    else:
        logger.debug(f"User {request.user.id} has no discord_id set")

    context = {
        'total_members': total_members,
        'recent_members': recent_members,
        'recent_posts': recent_posts,
        'member': member,
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)

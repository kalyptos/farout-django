"""
Core views for Farout application.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.members.models import Member
from apps.blog.models import BlogPost


def health_check(request):
    """Health check endpoint for Docker and monitoring."""
    return JsonResponse({
        'status': 'ok',
        'service': 'farout-django',
        'version': '1.0.0'
    })


def home(request):
    """Home/landing page."""
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]

    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """Main dashboard for authenticated users."""
    # Get organization stats
    total_members = Member.objects.count()
    recent_members = Member.objects.order_by('-created_at')[:5]
    recent_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:5]

    # Get user-specific data
    user = request.user
    try:
        member = Member.objects.get(discord_id=user.discord_id)
    except Member.DoesNotExist:
        member = None

    context = {
        'total_members': total_members,
        'recent_members': recent_members,
        'recent_posts': recent_posts,
        'member': member,
        'user': user,
    }
    return render(request, 'dashboard.html', context)

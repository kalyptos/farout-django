"""
Blog views for news and announcements.
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import BlogPost, Category, Tag


def blog_list(request):
    """
    Display list of blog posts with optional filtering by category or tag.
    """
    # Get query parameters
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('q')

    # Base queryset - only published posts
    posts = BlogPost.objects.filter(published=True).select_related('author', 'category').prefetch_related('tags')

    # Filter by category
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Filter by tag
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    # Search functionality
    if search_query:
        posts = posts.filter(
            Q(heading__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page (3x3 grid)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Get categories with post counts for sidebar
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    ).filter(post_count__gt=0)

    # Get recent posts for sidebar (excluding current page posts)
    recent_posts = BlogPost.objects.filter(published=True).exclude(
        id__in=[post.id for post in page_obj]
    )[:3]

    # Get popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    ).filter(post_count__gt=0).order_by('-post_count')[:10]

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag_slug,
    }

    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """
    Display a single blog post.
    """
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        published=True
    )

    # Get related posts (same category, excluding current post)
    related_posts = BlogPost.objects.filter(
        published=True,
        category=post.category
    ).exclude(id=post.id)[:3]

    # Get categories with post counts for sidebar
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    ).filter(post_count__gt=0)

    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]

    # Get popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__published=True))
    ).filter(post_count__gt=0).order_by('-post_count')[:10]

    context = {
        'post': post,
        'related_posts': related_posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
    }

    return render(request, 'blog/blog_detail.html', context)

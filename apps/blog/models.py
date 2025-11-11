"""
Blog post model for organization news and announcements.
"""
from __future__ import annotations
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField
from typing import Any


class BlogPost(models.Model):
    """
    Blog post model with rich text content and auto-generated slugs.
    """

    heading = models.CharField(
        max_length=255,
        help_text='Blog post title'
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='URL-friendly slug (auto-generated from title)'
    )

    content = HTMLField(
        help_text='Rich text content (HTML via TinyMCE)'
    )

    # CHANGED: CASCADE to PROTECT to prevent accidental data loss
    # If you need to delete a user, first reassign or delete their posts manually
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # Prevent deleting user if they have posts
        related_name='blog_posts',
        help_text='Post author (user cannot be deleted while having posts)'
    )

    feature_image = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Featured image URL'
    )

    published = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Is post published and visible?'
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['published', '-created_at']),
        ]

    def __str__(self) -> str:
        """Return string representation of blog post.

        Returns:
            str: Blog post heading/title
        """
        return self.heading

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Auto-generate unique slug from heading if not provided.

        Handles slug collisions by appending a counter.

        Args:
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments
        """
        if not self.slug:
            base_slug = slugify(self.heading)
            self.slug = base_slug
            counter = 1

            # Handle slug collisions
            while BlogPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

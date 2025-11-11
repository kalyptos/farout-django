"""
Blog post model for organization news and announcements.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField


class BlogPost(models.Model):
    """
    Blog post model with rich text content.
    """

    heading = models.CharField(
        max_length=255,
        help_text='Blog post title'
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='URL-friendly slug'
    )

    content = HTMLField(
        help_text='Rich text content (HTML)'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text='Post author'
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
        help_text='Is post published?'
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

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        """Auto-generate slug from heading if not provided."""
        if not self.slug:
            self.slug = slugify(self.heading)
        super().save(*args, **kwargs)

"""
Blog post model for organization news and announcements.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from tinymce.models import HTMLField


class Category(models.Model):
    """Blog post category."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        db_table = 'blog_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog post tag."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'blog_tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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

    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text='Short excerpt for previews'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text='Post author'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        help_text='Post category'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        help_text='Post tags'
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

    def get_absolute_url(self):
        """Get the URL for this blog post."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Auto-generate slug from heading if not provided."""
        if not self.slug:
            self.slug = slugify(self.heading)
        super().save(*args, **kwargs)

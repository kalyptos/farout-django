"""
Admin configuration for BlogPost model.
"""
from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for blog posts."""

    list_display = ('heading', 'author', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'created_at', 'author')
    search_fields = ('heading', 'content', 'slug')
    prepopulated_fields = {'slug': ('heading',)}
    ordering = ('-created_at',)

    fieldsets = (
        ('Content', {
            'fields': ('heading', 'slug', 'content', 'feature_image')
        }),
        ('Metadata', {
            'fields': ('author', 'published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    actions = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        """Bulk action to publish posts."""
        queryset.update(published=True)
        self.message_user(request, f'{queryset.count()} post(s) published.')
    publish_posts.short_description = 'Publish selected posts'

    def unpublish_posts(self, request, queryset):
        """Bulk action to unpublish posts."""
        queryset.update(published=False)
        self.message_user(request, f'{queryset.count()} post(s) unpublished.')
    unpublish_posts.short_description = 'Unpublish selected posts'

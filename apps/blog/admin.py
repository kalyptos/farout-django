"""
Admin configuration for BlogPost model.
"""
from django.contrib import admin
from .models import BlogPost, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for categories."""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for tags."""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for blog posts."""

    list_display = ('heading', 'category', 'author', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'category', 'created_at', 'author')
    search_fields = ('heading', 'content', 'slug')
    prepopulated_fields = {'slug': ('heading',)}
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Content', {
            'fields': ('heading', 'slug', 'content', 'feature_image')
        }),
        ('Classification', {
            'fields': ('category', 'tags')
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

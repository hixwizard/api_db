from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Reviews, Comment


class CategoryAdmin(admin.ModelAdmin):
    """Административня панель категорий."""
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    """Административная панель жанров."""
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_links = ('name',)


class TitleAdmin(admin.ModelAdmin):
    """Административная панель названий."""
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category', 'genre',)
    list_display_links = ('name',)


class GenreTitleAdmin(admin.ModelAdmin):
    """Административная панель жанра-произведения."""
    list_display = ('genre', 'title')
    search_fields = ('title',)
    list_display_links = ('title',)


class ReviewsAdmin(admin.ModelAdmin):
    """Административная панель отзывов."""
    list_display = (
        'title_id',
        'text',
        'score',
        'author'
    )
    search_fields = ('author',)
    list_display_links = ('text',)


class CommentAdmin(admin.ModelAdmin):
    """Административная панель комментариев."""
    list_display = (
        'title_id',
        'text',
        'author',
    )
    search_fields = ('author',)
    list_display_links = ('text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from .models import Post, Comment, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Додаткове порожнє поле для нового коментаря


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'get_tags')  # Додано поле для тегів
    list_filter = ('author', 'created_at', 'tags')  # Фільтруємо за тегами, автором і датою
    search_fields = ('title', 'content', 'tags__name')  # Пошук по тегам
    inlines = [CommentInline]  # Додає коментарі до поста
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'tags', 'author')  # Теги можна вибирати вручну в адмінці
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Робить секцію згорнутою
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # Дати тільки для читання

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())  # Показує всі теги через кому
    get_tags.short_description = 'Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')  # Показує поля коментарів
    list_filter = ('created_at', 'author')  # Фільтри для коментарів
    search_fields = ('content',)  # Пошук по контенту коментаря


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Показує назви тегів
    search_fields = ('name',)  # Пошук по іменах тегів

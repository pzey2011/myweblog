from django.contrib import admin
from .models import Post, Tag, Comment

class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    inlines = [
        CommentInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)

# Register your models here.

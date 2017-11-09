from django.contrib import admin
from .models import Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)

# Register your models here.

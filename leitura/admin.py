from django.contrib import admin

from leitura.models import Post, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "status", "author", "created_at", "updated_at")
	search_fields = ("title", "summary", "content", "author__username")
	list_filter = ("status", "author")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "role")
	list_filter = ("role",)

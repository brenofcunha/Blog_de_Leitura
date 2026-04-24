from django.contrib import admin

from leitura.models import Book, Category, Post, Tag, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "status", "author", "published_at", "created_at", "updated_at")
	search_fields = ("title", "summary", "content", "author__username")
	list_filter = ("status", "author")
	filter_horizontal = ("categories", "tags")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "author_name", "status", "rating", "added_by", "created_at")
	search_fields = ("title", "author_name", "description", "added_by__username")
	list_filter = ("status", "added_by")
	filter_horizontal = ("categories", "tags")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "role")
	list_filter = ("role",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	search_fields = ("name", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	search_fields = ("name", "slug")

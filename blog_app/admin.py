from django.contrib import admin

from .models import Comment, Post, Topic


# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "slug",
        "display_topic",
        "created_on",
        "updated_on",
    )
    list_filter = (
        "author",
        "created_on",
        "updated_on",
    )
    search_fields = (
        "id",
        "title",
        "author",
        "slug",
        "display_topic",
        "created_on",
        "updated_on",
    )
    prepopulated_fields = {"slug": ("title",)}  # this create the slug field from the title field
    autocomplete_fields = ("topics",)  # to more simple select multiple choices
    list_display_links = (
        "id",
        "title",
        "author",
        "slug",
        "display_topic",
        "created_on",
        "updated_on",
    )
    list_per_page = 5
    ordering = ["-id"]
    save_as = True

    inlines = [
        CommentInline,
    ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ["name"]
    save_as = True
    list_per_page = 5


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "post",
        "created",
    )
    date_hierarchy = "created"
    list_filter = (
        "email",
        "post",
        "created",
    )
    search_fields = (
        "id",
        "email",
        "post",
        "created",
    )
    list_display_links = (
        "id",
        "email",
        "post",
        "created",
    )
    ordering = ["-created"]
    save_as = True
    list_per_page = 5

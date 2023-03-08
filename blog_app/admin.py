from django.contrib import admin

from .models import Comment, Post, Topic


# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "draft",
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
        "draft",
    )
    search_fields = (
        "id",
        "title",
        "author__username",
        "slug",
        "created_on",
        "updated_on",
        "draft",
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
        "draft",
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
        "active",
        "id",
        "email",
        "post",
        "created_on",
        "name",
        "body",
    )
    date_hierarchy = "created_on"
    list_filter = (
        "email",
        "post",
        "created_on",
        "active",
    )
    search_fields = (
        "id",
        "email",
        "post",
        "created_on",
        "active",
    )
    list_display_links = (
        "id",
        "active",
        "email",
        "post",
        "created_on",
    )
    ordering = ["-created_on"]
    save_as = True
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        update_fields = []
        if form.cleaned_data["active"] is True:
            update_fields.append("active")
            obj.save(update_fields=update_fields)
        else:
            obj.save()

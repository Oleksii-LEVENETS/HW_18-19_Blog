from django.contrib import admin
from .models import Post, Topic


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'slug', 'display_topic', 'created_on', 'updated_on',)
    list_filter = ('author', 'created_on', 'updated_on',)
    search_fields = ('id', 'title', 'author', 'slug', 'display_topic', 'created_on', 'updated_on',)
    prepopulated_fields = {'slug': ('title',)}  # this create the slug field from the title field
    autocomplete_fields = ('topics',)  # to more simple select multiple choices
    list_display_links = ('id', 'title', 'author', 'slug', 'display_topic', 'created_on', 'updated_on',)
    list_per_page = 5
    ordering = ['-id']
    save_as = True


# TagAdmin must define "search_fields", because it's referenced by PostAdmin.autocomplete_fields.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ['name']
    save_as = True
    list_per_page = 5


class PostInline(admin.TabularInline):  # ToDo: for Author
    model = Post
    extra = 0

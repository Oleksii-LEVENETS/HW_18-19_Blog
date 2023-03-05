from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Topic(models.Model):
    name = models.CharField("Topic", max_length=20)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """Returns the url to access a particular topic."""
        return reverse("blog_app:topic-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=254, db_index=True)  # db_index=True to speed up searches
    # O2M: One Author, Many Posts:
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=254, db_index=True)  # db_index=True to speed up searches
    content = models.TextField(max_length=10_000, help_text="Enter the content of your Post here")
    image = models.ImageField(upload_to="", blank=True, null=True)
    # M2M: Many Topics, Many Posts:
    topics = models.ManyToManyField(Topic, help_text="Select a Topic for this Post", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def display_topic(self):
        """Creates a string for the Topics. This is required to display Topics in Admin."""
        return ", ".join([topic.name for topic in self.topics.all()[:2]])

    display_topic.short_description = "Topic"

    def get_absolute_url(self):
        return reverse("blog_app:post-detail", args=[str(self.id)])

    def __str__(self):
        return self.title


# Comments
class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Comment by {self.name}"

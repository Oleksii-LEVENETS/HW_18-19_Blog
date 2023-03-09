import random

from blog_app.models import Comment, Post, Topic

from blog_users.models import BlogUser

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from faker import Faker

"""
class Topic(models.Model):
    name = models.CharField("Topic", max_length=20)


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
    draft = models.BooleanField(default=False)


class Comment(models.Model):
    name = models.CharField(max_length=50, default="anonymous")
    email = models.EmailField(max_length=100, default="anonymous@anonymous.com")
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # related_name vs "comment_set"
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField("is published", default=False)
"""


class Command(BaseCommand):
    help = "Creating fake 5 Topics, 20 Posts, 50 Comments"  # noqa: A003

    def handle(self, *args, **options):
        fake = Faker()
        list_topics = []
        list_posts = []
        list_comments = []

        # Creating 5 Topics
        for _ in range(5):
            topic_name = fake.word().capitalize()
            list_topics.append(
                Topic(
                    name=topic_name,
                )
            )

        Topic.objects.bulk_create(list_topics)
        topics_id = Topic.objects.values_list("id", flat=True)

        # Creating 20 Posts
        blogusers_id = BlogUser.objects.exclude(is_superuser=1).values_list("id", flat=True)

        for _ in range(20):
            title = fake.text(18)
            author = BlogUser.objects.get(pk=random.choice(blogusers_id))
            slug = slugify(title)
            content = fake.text(500)
            list_posts.append(
                Post(
                    title=title,
                    author=author,
                    slug=slug,
                    content=content,
                )
            )

        posts_created = Post.objects.bulk_create(list_posts)
        posts_id = Post.objects.values_list("id", flat=True)

        # Creating M2M Post-Topic
        for post in posts_created:
            topics_list = []
            for _ in range(random.choice([1, 2])):
                topics_list.append(random.choice(topics_id))
            if len(topics_list) > 1:
                post.topics.add(topics_list[0], topics_list[1])
            post.topics.add(topics_list[0])

        # Creating 50 Comments
        for _ in range(50):
            author = BlogUser.objects.get(pk=random.choice(blogusers_id))
            name = author.username
            email = author.email
            body = fake.text(50)
            post = Post.objects.get(pk=random.choice(posts_id))
            active = True
            list_comments.append(Comment(name=name, email=email, body=body, post=post, active=active))

        Comment.objects.bulk_create(list_comments)

        self.stdout.write(self.style.SUCCESS("Successfully created fake 5 Topics, 20 Posts, 50 Comments"))

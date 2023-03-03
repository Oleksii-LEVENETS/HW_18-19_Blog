from django.test import TestCase
from django.urls import reverse

from .models import Post
from blog_users.models import BlogUser


# Create your tests here.
class PostCreateViewTest(TestCase):
    def test_post_create_stores_user(self):
        user1 = BlogUser.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        post_data = {
            'title': 'test post',
            'content': 'Hello world',
        }
        self.client.force_login(user1)
        self.client.post(reverse('blog_app:post-create'), post_data)

        self.assertTrue(Post.objects.filter(author=user1).exists())


class PostUpdateViewTest(TestCase):
    def test_post_update_returns_404(self):
        user1 = BlogUser.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        user2 = BlogUser.objects.create_user(
            username='user2', email='user2@gmail.com', password='1234'
        )
        post = Post.objects.create(
            author=user1, title='test post', content='Hello world')

        self.client.force_login(user2)
        response = self.client.post(
            reverse('blog_app:post-update', kwargs=({'pk': post.id})),
            {'title': 'change title'}
        )
        self.assertEqual(response.status_code, 404)

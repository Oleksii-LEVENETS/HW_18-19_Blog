import tempfile
from PIL import Image
from django.test import override_settings, TestCase
from django.urls import reverse

from ..models import BlogUser, Profile
from ..forms import SignUpForm


# Create your tests here.
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSignUpView(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        self.data = {
            'username': 'test',
            'email': 'test@hotmail.com',
            'password1': 'test12345',
            'password2': 'test12345'
        }

    def test_signup_returns_200(self):
        response = self.client.get(reverse('blog_users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_users/signup.html')

    def test_user_is_logged_in(self):
        response = self.client.post(
            reverse('blog_users:signup'), self.data, follow=True
        )
        user = response.context.get('user')

        self.assertTrue(user.is_authenticated)

    def test_new_user_is_registered(self):
        nb_old_users = BlogUser.objects.count()
        self.client.post(reverse('blog_users:signup'), self.data)
        nb_new_users = BlogUser.objects.count()
        self.assertEqual(nb_new_users, nb_old_users + 1)

    def test_redirect_if_user_is_authenticated(self):
        login = self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('blog_users:signup'))

        self.assertRedirects(response, reverse('blog_app:index'))

    def test_invalid_form(self):
        response = self.client.post(reverse('blog_users:signup'), {
            "email": "test@admin.com",
            "password1": "test12345",
            "password2": "test12345",
        })
        form = response.context.get('form')

        self.assertFalse(form.is_valid())


# Testing the Profile View
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = BlogUser.objects.create_user(
            username="user1", email="user1@gmail.com", password="1234"
        )
        self.user2 = BlogUser.objects.create_user(
            username="user2", email="user2@gmail.com", password="1234"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(
            "blog_users:profile", kwargs=({"username": self.user1.username}))
        )

        self.assertRedirects(
            response, "/blog_users/login/?next=/blog_users/profile/user1/")

    def test_returns_200(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(reverse(
            "blog_users:profile", kwargs=({"username": self.user1.username})
        ))

        self.assertEqual(response.status_code, 200)

    def test_view_returns_profile_of_current_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(reverse(
            "blog_users:profile", kwargs=({"username": self.user1.username}))
        )
        self.assertEqual(response.context["user"], self.user1)
        self.assertEqual(response.context["profile"], self.user1.profile)

    def test_view_returns_profile_of_a_given_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(reverse(
            "blog_users:profile", kwargs=({"username": self.user2.username}))
        )
        self.assertEqual(response.context["user"], self.user2)
        self.assertEqual(response.context["profile"], self.user2.profile)


# Testing the Edit Profile View
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = BlogUser.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )

    def test_edit_profile_returns_200(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('blog_users:edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('blog_users:edit_profile'))
        self.assertRedirects(
            response, '/blog_users/login/?next=/blog_users/edit-profile/')

    def test_edit_profile_change_username(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.post(reverse('blog_users:edit_profile'), {
            'username': 'user2',
            'about_me': 'Hello world'
        })

        user2 = BlogUser.objects.filter(email='user1@gmail.com')[0]
        self.assertEqual(user2.username, 'user2')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image(self):
        login = self.client.login(email='user1@gmail.com', password='1234')
        image = self._create_image()
        profile = Profile.objects.get(user=self.user1)

        self.assertFalse(bool(profile.image))

        with open(image.name, 'rb') as f:
            response = self.client.post(reverse('blog_users:edit_profile'), {
                'username': 'user1',
                'about_me': 'Hello world',
                'image': f
            })
        profile.refresh_from_db()

        self.assertTrue(bool(profile.image))

    def _create_image(self):
        f = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        image = Image.new('RGB', (200, 200), 'white')
        image.save(f, 'PNG')

        return f

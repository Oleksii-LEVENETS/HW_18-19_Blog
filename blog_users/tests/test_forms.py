from django.test import TestCase

from ..forms import EditProfileForm
from ..models import BlogUser


class EditProfileFormTest(TestCase):
    def test_username_already_taken(self):
        BlogUser.objects.create_user(username="user1", email="user1@gmail.com", password="1234")
        form = EditProfileForm(data={"username": "user1", "about_me": "somthing about me"}, original_username="user")
        self.assertFalse(form.is_valid())

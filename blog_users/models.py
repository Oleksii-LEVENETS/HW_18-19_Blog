from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class BlogUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]


class Profile(models.Model):
    """
    This method results in additional queries, so in a real project, it is preferable to extend the BlogUser model.
    """

    about_me = models.TextField()
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.OneToOneField(BlogUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

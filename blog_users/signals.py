from blog_app import tasks
from blog_app.models import Comment, Post


from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import BlogUser, Profile


@receiver(post_save, sender=BlogUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        subject = f"User '{instance}' is created."
        message = f"User '{instance}' is created. Is Admin: {instance.is_superuser}. Is Staff: {instance.is_staff}."
        user_email = instance.email
        tasks.send_mail_temp.delay(subject, message, user_email)


@receiver(post_save, sender=Post)
def create_update_post(sender, instance, created, **kwargs):
    subject = f"Created/Updated Post. '{instance.title}'."
    if created:  # noqa: R505
        return
    else:
        if instance.draft:  # is True
            message = (
                f"Status Draft: {instance.draft}.\n"
                f"Your post '{instance}' is created/updated, but NOT PUBLISHED.\n"
                f"Content: '{instance.content}'"
            )
        else:
            message = (
                f"Status Draft: {instance.draft}.\n"
                f"Your post '{instance}' is created/updated and HAS PUBLISHED!\n"
                f"Content: '{instance.content}'."
            )
    user_email = instance.author.email
    tasks.send_mail_temp.delay(subject, message, user_email)


@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:
        subject = f"New Comment to {instance.post} | Created on {instance.created_on}."
        message = f"New Comment is created, but not published yet. Content: '{instance.body}'"
        user_email = instance.post.author.email
        tasks.send_mail_temp.delay(subject, message, user_email)


@receiver(post_save, sender=Comment)
def change_comment_to_active(sender, instance, update_fields, **kwargs):
    if update_fields:
        subject = f"Comment to {instance.post} Created on {instance.created_on} is published."
        current_site = get_current_site(request=None)
        site_name = current_site.name
        url = instance.get_absolute_url()
        message = site_name + url
        user_email = instance.post.author.email
        tasks.send_mail_temp.delay(subject, message, user_email)


# This code for S3 file deletion
@receiver(pre_delete, sender=Post)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

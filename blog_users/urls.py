from blog_core import settings

from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from .views import edit_profile, log_in, log_out, profile, signup


app_name = "blog_users"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", log_in, name="login"),
    path("logout/", log_out, name="logout"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="blog_users/password_reset.html",
            email_template_name="blog_users/password_reset_email.html",
            subject_template_name="blog_users/password_reset_subject.txt",
            success_url="/blog_users/password_reset/done/",
            from_email=settings.EMAIL_HOST_USER,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="blog_users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="blog_users/password_reset_confirm.html", success_url="/blog_users/reset/done/"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="blog_users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("profile/<username>/", profile, name="profile"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="blog_users/password_change.html",
            success_url=reverse_lazy("blog_users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="blog_users/password_change_done.html"),
        name="password_change_done",
    ),
]

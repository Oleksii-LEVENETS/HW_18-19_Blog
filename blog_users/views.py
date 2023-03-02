from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EditProfileForm, LoginForm, SignUpForm
from .models import BlogUser, Profile


# Create your views here.
def signup(request):
    # redirect a user to the home page if he is already logged in
    if request.user.is_authenticated:
        return redirect('blog_app:index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Congratulations, you are now a registered User!")
            return redirect('blog_app:index')
    else:
        form = SignUpForm()
    return render(request, 'blog_users/signup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('blog_app:index')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('blog_app:index')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'blog_users/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('blog_users:login'))


@login_required
def profile(request, username):
    user = get_object_or_404(BlogUser, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'blog_users/profile.html', {'profile': profile, 'user': user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user.username, request.POST, request.FILES)

        if form.is_valid():
            about_me = form.cleaned_data["about_me"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]

            user = BlogUser.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about_me = about_me
            if image:
                profile.image = image
            profile.save()
            return redirect("blog_users:profile", username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, "blog_users/edit_profile.html", {'form': form})

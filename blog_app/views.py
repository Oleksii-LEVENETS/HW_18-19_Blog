from blog_users.models import BlogUser

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, ContactForm
from .models import Post, Topic


# Create your views here.
class Index(ListView):
    template_name = "blog_app/index.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["num_posts"] = Post.objects.count()
        context["num_topics"] = Topic.objects.count()
        context["num_users"] = BlogUser.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(draft=False).filter(active=True)


class PostListView(ListView):
    template_name = "blog_app/post_list.html"
    model = Post
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return Post.objects.filter(draft=False).filter(active=True)


class TopicListView(ListView):
    template_name = "blog_app/topic_list.html"
    model = Topic
    paginate_by = 10


def PostDetailView(request, pk):  # noqa: N802
    template_name = "blog_app/post_detail.html"
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)  # post = models.ForeignKey(... related_name="comments")
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Your comment has been sent to Admin for checking!")
            subject = "New comment saved."
            message = new_comment
            user_email = request.user.email
            send_mail_temp(subject, message, user_email)
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {"post": post, "comments": comments, "new_comment": new_comment, "comment_form": comment_form},
    )


class TopicDetailView(DetailView):
    template_name = "blog_app/topic_detail.html"
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        posts = (
            Post.objects.prefetch_related("topics")
            .filter(topics__id=self.object.id)
            .filter(draft=False)
            .filter(active=True)
        )
        context["posts"] = posts
        return context


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog_app/post_list.html"
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return Post.objects.filter(author=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mypost = True
        context["mypost"] = mypost
        return context


# Users' Posts: create, edit, and delete posts.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "topics", "draft"]

    def get_success_url(self):
        messages.success(self.request, "Your post was created successfully!")
        return reverse_lazy("blog_app:index")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data["title"])
        obj.draft = form.cleaned_data["draft"]
        obj.active = False
        obj.save()
        if not obj.draft:
            subject = f"New Post '{obj.title}' created."
            message = obj.content
            user_email = self.request.user.email
            send_mail_temp(subject, message, user_email)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "topics", "draft"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context["update"] = update
        return context

    def get_success_url(self):
        messages.success(self.request, "Your post has been updated successfully.")
        return reverse_lazy("blog_app:index")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.active = False
        obj.save()
        if not obj.draft:
            subject = f"Updated Post '{obj.title}'."
            message = obj.content
            user_email = self.request.user.email
            send_mail_temp(subject, message, user_email)
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(self.request, "Your post has been deleted successfully.")
        return reverse_lazy("blog_app:index")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(author=self.request.user)


# Contact Us
def email_contact_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.send_email()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
    else:
        form = ContactForm(initial={"first_name": "User", "last_name": "Userenko", "email_address": "uu@example.com"})
    return email_contact_form(request, form, "blog_app/partial_contact_form_create.html")


def send_mail_temp(subject, message, user_email):
    email_to = ["admin@admin.com", user_email]
    try:
        send_mail(
            f"{subject}",
            f"{message}",
            "admin@admin.com",
            email_to,
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")

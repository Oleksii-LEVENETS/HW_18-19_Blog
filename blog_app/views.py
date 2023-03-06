from blog_users.models import BlogUser

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
from .models import Comment, Post, Topic


# Create your views here.
class Index(ListView):
    template_name = "blog_app/index.html"
    queryset = Post.objects.select_related("author").prefetch_related("topics").all()
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


class PostListView(ListView):
    template_name = "blog_app/post_list.html"
    model = Post
    queryset = Post.objects.all()
    paginate_by = 2


class TopicListView(ListView):
    template_name = "blog_app/topic_list.html"
    model = Topic
    paginate_by = 3


class PostDetailView(DetailView):
    template_name = "blog_app/post_detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all()

        context["post"] = post
        context["comments"] = comments
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.select_related("author").prefetch_related("topics").filter(id=self.kwargs["pk"])[0]
        comments = post.comment_set.all()

        context["post"] = post
        context["comments"] = comments
        context["form"] = form

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            content = form.cleaned_data["content"]

            comment = Comment.objects.create(name=name, email=email, content=content, post=post)  # noqa: F841

            form = CommentForm()
            context["form"] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class TopicDetailView(DetailView):
    template_name = "blog_app/topic_detail.html"
    model = Topic


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog_app/post_list.html"
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.id)


# Users' Posts: create, edit, and delete posts.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "topics"]

    def get_success_url(self):
        messages.success(self.request, "Your post has been created successfully.")
        return reverse_lazy("blog_app:index")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data["title"])
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "topics"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context["update"] = update
        return context

    def get_success_url(self):
        messages.success(self.request, "Your post has been updated successfully.")
        return reverse_lazy("blog_app:index")

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

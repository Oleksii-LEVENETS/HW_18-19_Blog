from blog_core import settings

from blog_users.models import BlogUser

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
from .models import Comment, Post, Topic


# Create your views here.
class Index(ListView):
    template_name = "blog_app/index.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["num_posts"] = Post.objects.filter(draft=False).count()
        context["num_topics"] = Topic.objects.count()
        context["num_users"] = BlogUser.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.select_related("author").prefetch_related("topics").all()
        return Post.objects.select_related("author").prefetch_related("topics").filter(draft=False)


class PostListView(ListView):
    template_name = "blog_app/post_list.html"
    model = Post
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.select_related("author").prefetch_related("topics").all()
        return Post.objects.select_related("author").prefetch_related("topics").filter(draft=False)


class TopicListView(ListView):
    template_name = "blog_app/topic_list.html"
    model = Topic
    paginate_by = 3


def PostDetailView(request, pk):  # noqa: N802
    template_name = "blog_app/post_detail.html"
    post = get_object_or_404(Post, pk=pk)
    comms = post.comments.filter(active=True)  # post = models.ForeignKey(... related_name="comments")
    # comms = Comment.objects.filter(active=True).filter(post__pk=post.pk)
    comms_num = Comment.objects.filter(active=True).filter(post__pk=post.pk).count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if not new_comment.name:
                new_comment.name = "anonymous"
            if not new_comment.email:
                new_comment.email = "anonymous@anonymous.com"
            new_comment.save()
            messages.success(request, "Your comment was created successfully!")
    else:
        comment_form = CommentForm()

    page = request.GET.get("page", 1)
    paginator = Paginator(comms, per_page=1)
    try:
        comms = paginator.page(page)
    except PageNotAnInteger:
        comms = paginator.page(1)
    except EmptyPage:
        comms = paginator.page(paginator.num_pages)

    return render(
        request,
        template_name,
        {
            "post": post,
            "comms": comms,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "comms_num": comms_num,
        },
    )


class TopicDetailView(DetailView):
    template_name = "blog_app/topic_detail.html"
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(topics__id=self.object.id).filter(draft=False)
        context["posts"] = posts
        return context


class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog_app/post_list.html"
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.select_related("author").prefetch_related("topics").all()
        return Post.objects.select_related("author").prefetch_related("topics").filter(author=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mypost = True
        context["mypost"] = mypost
        return context


# Users' Posts: create, edit, and delete posts.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog_app/post_form.html"
    fields = ["title", "content", "image", "topics", "draft"]

    def get_success_url(self):
        messages.success(self.request, "Your post was created successfully!")
        return reverse_lazy("blog_app:index")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data["title"])
        obj.draft = form.cleaned_data["draft"]
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog_app/post_form.html"
    fields = ["title", "content", "image", "topics", "draft"]

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
            subject = "Website Inquiry."
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())
            send_mail_temp(subject, message)
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
        # form = ContactForm(initial={"first_name": "User", "last_name": "Usenko", "email_address": "uu@example.com"})
        form = ContactForm()
    return email_contact_form(request, form, "blog_app/partial_contact_form_create.html")


def send_mail_temp(subject, message, user_email=None):
    email_to = [settings.EMAIL_HOST_USER, user_email]
    if user_email is None:
        email_to = [settings.EMAIL_HOST_USER]
    try:
        send_mail(
            subject=f"{subject}",
            message=f"{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_to,
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")

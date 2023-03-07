from blog_app import views

from django.urls import path


app_name = "blog_app"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("posts/", views.PostListView.as_view(), name="posts"),
    path("myposts/", views.MyPostsListView.as_view(), name="my-posts"),
    path("topics/", views.TopicListView.as_view(), name="topics"),
    path("topic_detail/<int:pk>", views.TopicDetailView.as_view(), name="topic-detail"),
    path("post_detail/<int:pk>/", views.PostDetailView, name="post-detail"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post_update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("post_delete/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("contact/", views.contact, name="contact"),
]

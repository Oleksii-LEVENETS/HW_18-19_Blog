from django.urls import path

from blog_app import views


app_name = "blog_app"

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    path('posts/', views.PostListView.as_view(), name='posts'),
    path('myposts/', views.MyPostsListView.as_view(), name='my-posts'),
    
    path('topics/', views.TopicListView.as_view(), name='topics'),

    path('topic_detail/<int:pk>', views.TopicDetailView.as_view(), name='topic-detail'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),


    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('post_delete/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),


    # path('post/<int:pk>/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    
    # path('books/', views.BookListView.as_view(), name='books'),
    # path('authors/', views.AuthorListView.as_view(), name='authors'),
    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    #
    # path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # path('all_borrowed_books/', views.AllLoanedBooksListView.as_view(), name='all-borrowed-books'),
    #
    # path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    #
    # path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    # path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    # path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    #
    # path('book/create/', views.BookCreate.as_view(), name='book-create'),
    # path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    # path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

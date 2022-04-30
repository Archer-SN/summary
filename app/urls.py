from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # List of articles and books
    path("books", views.book_lists, name="books"),
    path("articles", views.article_lists, name="articles"),
    # User's profile view
    path("user", views.user_view, name="user"),
    # Views articles and books the user have created
    path("books/<str:username>/<slug:book_name>", views.book_view, name="book"),
    path("articles/<str:username>/<slug:article_name>",
         views.article_view, name="article"),

    path("create", views.create, name="create")
]

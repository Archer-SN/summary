from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),

    # List of articles and books
    path("books", views.book_list, name="books"),
    path("articles", views.article_list, name="articles"),
    # User's profile view
    path("user/<str:username>", views.user_view, name="user"),
    # Views articles and books the user have created
    path("books/<int:book_id>", views.book_view, name="book"),
    path("articles/<int:article_id>",
         views.article_view, name="article"),

    path("create/book", views.create_book, name="create_book"),
    path("create/article", views.create_article, name="create_article"),

    path("edit/book/<int:book_id>", views.edit_book, name="edit_book"),
    path("edit/article<int:article_id>",
         views.edit_article, name="edit_article"),

    path("comment", views.comment, name="comment"),

    path("error", views.error_view, name="error")
]

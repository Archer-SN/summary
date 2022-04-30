from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    favorite_books = models.ManyToManyField(
        "Book", related_name="user_favorited")
    favorite_articles = models.ManyToManyField(
        "Article", related_name="user_favorited")
    reading_books = models.ManyToManyField(
        "Book", related_name="user_read")
    reading_articles = models.ManyToManyField(
        "Article", related_name="user_read")
    finished_books = models.ManyToManyField(
        "Book", related_name="user_finished")
    finished_articles = models.ManyToManyField(
        "Article", related_name="user_finished")


class Category(models.Model):
    name = models.CharField(max_length=32)


class ContentModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField()

    class Meta:
        abstract = True


class Book(ContentModel):
    name = models.CharField(max_length=64)


class Article(ContentModel):
    name = models.CharField(max_length=64)


class BookComment(ContentModel):
    parent = models.ForeignKey(Book, on_delete=models.CASCADE)


class ArticleComment(ContentModel):
    parent = models.ForeignKey(Article, on_delete=models.CASCADE)

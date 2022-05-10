from os import stat
from telnetlib import STATUS
from markdown2 import markdown
from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_picture = models.URLField(
        default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    favorite_books = models.ManyToManyField(
        "Book", related_name="user_favorited", blank=True)
    favorite_articles = models.ManyToManyField(
        "Article", related_name="user_favorited", blank=True)
    reading_books = models.ManyToManyField(
        "Book", related_name="user_read", blank=True)
    finished_books = models.ManyToManyField(
        "Book", related_name="user_finished", blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=32)
    # Font awesome's icon name
    icon = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name


class ContentModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def formatted_time(self):
        return self.date_created.strftime("%d %B %Y")

    def html_content(self):
        return markdown(self.content)


class Book(ContentModel):
    # author is the person who summarized the book
    # book_author is the person who wrote the book
    book_author = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    thumbnail = models.URLField(default='')
    category = models.ManyToManyField(Category)

    def all_published():
        return Article.objects.filter(status=True)

    def all_categories():
        return Category.objects.filter(id__in=Book.objects.all().values("category")).exclude(name="All").distinct()

    def json_data(self):
        return {"id": self.id, "author": self.author.username, "thumbnail": self.thumbnail, "date_created": self.formatted_time, "book_author": self.book_author, "title": self.title, "category": self.category.first().name}

    def __str__(self):
        return f"{self.title} summarized by {self.author.username}"


class Article(ContentModel):
    title = models.CharField(max_length=64)
    thumbnail = models.URLField(default='')
    category = models.ManyToManyField(Category)

    def all_categories():
        return Category.objects.filter(id__in=Article.objects.all().values("category")).exclude(name="All").distinct()

    def json_data(self):
        return {"id": self.id, "author": self.author.username, "thumbnail": self.thumbnail, "date_created": self.formatted_time, "title": self.title, "category": self.category.first().name}

    def __str__(self):
        return f"{self.title} wrote by {self.author.username}"


class BookComment(ContentModel):
    parent = models.ForeignKey(Book, on_delete=models.CASCADE)


class ArticleComment(ContentModel):
    parent = models.ForeignKey(Article, on_delete=models.CASCADE)


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "thumbnail", "category", "content"]

    def __init__(self, *args, **kwargs):
        super(NewArticleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['autocomplete'] = 'off'


class NewBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["title", "book_author", "thumbnail", "category", "content"]

    def __init__(self, *args, **kwargs):
        super(NewBookForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['autocomplete'] = 'off'

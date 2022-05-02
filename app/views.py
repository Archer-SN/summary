from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Category, Book, Article, BookComment
# Create your views here.


class NewArticleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    thumbnail = forms.URLField()
    title = forms.CharField(max_length=64)

    CATEGORY_CHOICES = ((article_category, article_category)
                        for article_category in Category.objects.all())
    categories = forms.ChoiceField(choices=CATEGORY_CHOICES)


class NewBookForm(forms.Form):
    book_author = forms.CharField(max_length=64)
    content = forms.CharField(widget=forms.Textarea)
    thumbnail = forms.URLField()
    title = forms.CharField(max_length=64)

    CATEGORY_CHOICES = ((book_category, book_category)
                        for book_category in Category.objects.all())
    categories = forms.ChoiceField(choices=CATEGORY_CHOICES)


def index(request):
    return render(request, "app/index.html", {
        "new_books": Book.objects.all()[:2],
        "new_articles": Article.objects.all()[:3]})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


def book_list(request):

    return render(request, "app/list.html", {
        "content_type": "book",
        "content_list": Book.objects.all(),
        "categories": Book.all_categories()
    })


def article_list(request):
    return render(request, "app/list.html", {
        "content_type": "article",
        "content_list": Article.objects.all(),
        "categories": Article.all_categories()
    })


def user_view(request, username):
    return render(request, "app/profile.html", {

    })


def book_view(request, username, book_name):
    pass


def article_view(request, username, article_name):
    pass


def create_book(request):
    if request.method == "POST":
        book_form = NewBookForm(request.POST)
        if book_form.is_valid():
            book_author = book_form.cleaned_data["book_author"]
            content = book_form.cleaned_data["content"]
            thumbnail = book_form.cleaned_data["thumbnail"]
            title = book_form.cleaned_data["title"]
            categories = book_form.cleaned_data["categories"]
            new_book = Book.objects.create(author=request.user, book_author=book_author, content=content,
                                           thumbnail=thumbnail, title=title)
            new_book.category.set(
                Category.objects.filter(name=categories))

            return HttpResponseRedirect(reverse("books"))

    else:
        book_form = NewBookForm()

    return render(request, "app/create.html", {
        "content_type": "book",
        "form": book_form,
    })


def create_article(request):
    if request.method == "POST":
        article_form = NewArticleForm(request.POST)
        if article_form.is_valid():
            content = article_form.cleaned_data["content"]
            thumbnail = article_form.cleaned_data["thumbnail"]
            title = article_form.cleaned_data["title"]
            categories = article_form.cleaned_data["categories"]
            new_article = Article.objects.create(author=request.user, content=content,
                                                 thumbnail=thumbnail, title=title)
            new_article.category.set(
                Category.objects.filter(name=categories))

            return HttpResponseRedirect(reverse("articles"))
    else:
        article_form = NewArticleForm()

    return render(request, "app/create.html", {
        "content_type": "article",
        "form": article_form,
    })

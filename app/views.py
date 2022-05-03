import json
from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Category, Book, Article, BookComment, NewArticleForm, NewBookForm
# Create your views here.


def index(request):
    return render(request, "app/index.html", {
        "new_books": Book.objects.all().order_by("-id")[:2],
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


def book_view(request, book_id):
    if not Book.objects.filter(pk=book_id).exists():
        return HttpResponseRedirect(reverse("error"))

    return render(request, "app/content.html", {
        "content_type": "book",
        "content": Book.objects.get(pk=book_id)
    })


def article_view(request, article_id):
    if not Article.objects.filter(pk=article_id).exists():
        return HttpResponseRedirect(reverse("error"))

    return render(request, "app/content.html", {
        "content_type": "article",
        "content": Article.objects.get(pk=article_id)
    })


@login_required
def create_book(request):
    if request.method == "POST":
        # The author field is not provided in the form
        book = Book(author=request.user)
        book_form = NewBookForm(request.POST, instance=book)

        if book_form.is_valid():
            book_form.save()
            return HttpResponseRedirect(reverse("books"))

    else:
        book_form = NewBookForm()

    return render(request, "app/form.html", {
        "value": "Create",
        "form": book_form,
    })


@login_required
def create_article(request):
    if request.method == "POST":
        # The author field is not provided in the form
        article = Article(author=request.user)
        article_form = NewArticleForm(request.POST, instance=article)

        if article_form.is_valid():
            article_form.save()

            return HttpResponseRedirect(reverse("articles"))
    else:
        article_form = NewArticleForm()

    return render(request, "app/form.html", {
        "value": "Create",
        "form": article_form,
    })


@login_required
def edit_book(request, book_id):
    # Edit the book
    if request.method == "POST":

        if not Book.objects.filter(pk=book_id).exists():
            return HttpResponseRedirect(reverse("error"))

        book = Book.objects.get(pk=book_id)

        if book.author.id != request.user.id:
            return HttpResponse(status=401)

        book_form = NewBookForm(request.POST, instance=book)
        if book_form.is_valid():
            book_form.save()
            return HttpResponseRedirect(reverse("book", args=[book_id]))

    elif request.method == "GET":
        # Send a form with a populated data if the book exists
        if Book.objects.filter(pk=book_id).exists():
            book = Book.objects.get(pk=book_id)

            if request.user.id != book.author.id:
                return HttpResponse(status=401)

            book_form = NewBookForm(instance=book)
            return render(request, "app/form.html", {
                "value": "Save",
                "form": book_form,
            })
        else:
            return HttpResponseRedirect(reverse("error"))

    else:
        return HttpResponse(status=405)


@login_required
def edit_article(request, article_id):
    # Edit the article
    if request.method == "POST":

        if not Article.objects.filter(pk=article_id).exists():
            return HttpResponseRedirect(reverse("error"))

        article = Article.objects.get(pk=article_id)

        if article.author.id != request.user.id:
            return HttpResponse(status=401)

        article_form = NewArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse("article", args=[article_id]))

    elif request.method == "GET":
        # Send a form with a populated data if the book exists
        if article.objects.filter(pk=article_id).exists():
            article = Article.objects.get(pk=article_id)

            if request.user.id != article.author.id:
                return HttpResponse(status=401)

            article_form = NewArticleForm(instance=article)
            return render(request, "app/form.html", {
                "value": "Save",
                "form": article_form,
            })
        else:
            return HttpResponseRedirect(reverse("error"))

    else:
        return HttpResponse(status=405)


def error_view(request):
    return render(request, "app/error.html")

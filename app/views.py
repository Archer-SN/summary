import json
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import User, Category, Book, Article, BookComment, ArticleComment, NewArticleForm, NewBookForm
# Create your views here.


@login_required
def index(request):

    return render(request, "app/index.html", {
        "new_books": Book.objects.defer("content").all().order_by("-id")[:2],
        "new_articles": Article.objects.defer("content").all()[:3],
        "favorite_books": Book.objects.defer("content").filter(pk__in=request.user.favorite_books.all()),
        "reading_books": Book.objects.defer("content").filter(pk__in=request.user.reading_books.all()),
        "finished_books": Book.objects.defer("content").filter(pk__in=request.user.finished_books.all())})


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
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


def book_list(request):

    # Value to sort by
    # Sort by latest by default
    search_value = request.GET.get("search", None)
    sort_value = request.GET.get("sort", None)
    category_value = request.GET.get("category", "undefined")
    if sort_value != None or search_value != None:
        # Sort value can not be an empty string
        if sort_value == None or sort_value == "":
            sort_value = "-date_created"
        if search_value == None:
            search_value = ""

        content_list = []
        if not category_value or category_value == "undefined":
            for book in Book.objects.all().filter(title__contains=search_value).order_by(sort_value):
                content_list.append(book.json_data(
                ) | {"favorite": request.user.favorite_books.filter(pk=book.id).exists()})
        else:
            for book in Book.objects.all().filter(title__contains=search_value).filter(category__id=Category.objects.get(name=category_value).id).order_by(sort_value):
                content_list.append(book.json_data(
                ) | {"favorite": request.user.favorite_books.filter(pk=book.id).exists()})

        return JsonResponse({"content_type": "book",
                             "content_list": content_list})

    return render(request, "app/list.html", {
        "content_type": "book",
        "content_list": Book.objects.defer("content").all().order_by("-date_created"),
        "categories": Book.all_categories()
    })


def article_list(request):

    # Value to sort by
    # Sort by latest by default
    search_value = request.GET.get("search", None)
    sort_value = request.GET.get("sort", None)
    category_value = request.GET.get("category", "undefined")
    if sort_value != None or search_value != None:
        # Sort value can not be an empty string
        if sort_value == None or sort_value == "":
            sort_value = "-date_created"
        if search_value == None:
            search_value = ""

        content_list = []
        if not category_value or category_value == "undefined":
            for article in Article.objects.all().filter(title__contains=search_value).order_by(sort_value):
                content_list.append(article.json_data(
                ) | {"favorite": request.user.favorite_articles.filter(pk=article.id).exists()})
        else:
            for article in Article.objects.all().filter(title__contains=search_value).filter(category__id=Category.objects.get(name=category_value).id).order_by(sort_value):
                content_list.append(article.json_data(
                ) | {"favorite": request.user.favorite_articles.filter(pk=article.id).exists()})

        return JsonResponse({"content_type": "article",
                             "content_list": content_list})

    return render(request, "app/list.html", {
        "content_type": "article",
        "content_list": Article.objects.defer("content").all().order_by("-date_created"),
        "categories": Article.all_categories()
    })


def user_view(request, username):
    if not User.objects.filter(username=username).exists():
        return HttpResponseRedirect(reverse("error"))
    user = User.objects.get(username=username)
    return render(request, "app/profile.html", {
        "user": user,
        "summarized_books": Book.objects.filter(author=user),
        "written_articles": Article.objects.filter(author=user)
    })


def book_view(request, book_id):
    # Handling favorites
    if request.method == "PUT":
        data = json.loads(request.body)
        action = data["action"]
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        book = Book.objects.get(pk=book_id)

        if not book:
            return HttpResponse(status=404)

        if action == "favorite":
            # If book is already favorited
            if request.user.favorite_books.filter(pk=book_id).exists():
                request.user.favorite_books.remove(book)
                return JsonResponse({"className": "not-favorite"})
            else:
                request.user.favorite_books.add(book)
                return JsonResponse({"className": "is-favorite"})
        # Add to currently reading list
        elif action == "reading":
            if request.user.reading_books.filter(pk=book_id).exists():
                return HttpResponse(status=304)

            request.user.finished_books.remove(book)
            request.user.reading_books.add(book)
            return HttpResponse(status=201)
        # Add to finished
        elif action == "finished":
            if request.user.finished_books.filter(pk=book_id).exists():
                return HttpResponse(status=304)

            # The book can only be in one place either reading or finished
            request.user.finished_books.add(book)
            request.user.reading_books.remove(book)
            return HttpResponse(status=201)
        # Remove from list
        elif action == "remove":
            if data["from"] == "favorites":
                request.user.favorite_books.remove(book)
            else:
                request.user.finished_books.remove(book)
                request.user.reading_books.remove(book)
            return HttpResponse(status=201)

    else:
        if not Book.objects.filter(pk=book_id).exists():
            return HttpResponseRedirect(reverse("error"))

        return render(request, "app/content.html", {
            "content_type": "book",
            "content": Book.objects.get(pk=book_id),
            "comments": BookComment.objects.filter(parent__id=book_id).order_by("-date_created"),
        })


def article_view(request, article_id):

    if request.method == "PUT":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        # If article is already favorited
        if request.user.favorite_articles.filter(pk=article_id).exists():
            request.user.favorite_articles.remove(
                Article.objects.get(pk=article_id))
            return JsonResponse({"className": "not-favorite"})
        else:
            request.user.favorite_articles.add(
                Article.objects.get(pk=article_id))
            return JsonResponse({"className": "is-favorite"})

    else:
        if not Article.objects.filter(pk=article_id).exists():
            return HttpResponseRedirect(reverse("error"))

        return render(request, "app/content.html", {
            "content_type": "article",
            "content": Article.objects.get(pk=article_id),
            "comments": ArticleComment.objects.filter(parent__id=article_id).order_by("-date_created"),
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
        if Article.objects.filter(pk=article_id).exists():
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


def comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content_type = data["content_type"]
        content = data["content"]
        content_id = data["content_id"]

        if len(content) <= 0:
            return HttpResponse(status=400)

        if content_type == "book":
            if not Book.objects.filter(pk=content_id).exists():
                return HttpResponse(status=404)
            BookComment.objects.create(
                author=request.user, content=content, parent=Book.objects.get(pk=content_id))
            return HttpResponse(status=201)
        elif content_type == "article":
            if not Article.objects.filter(pk=content_id).exists():
                return HttpResponse(status=404)
            ArticleComment.objects.create(
                author=request.user, content=content, parent=Article.objects.get(pk=content_id))
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
    elif request.method == "PUT":
        pass
    else:
        return HttpResponse(status=405)


def error_view(request):
    return render(request, "app/error.html")

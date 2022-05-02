from django.contrib import admin
from .models import User, Category, Book, Article, BookComment, ArticleComment

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Article)
admin.site.register(BookComment)
admin.site.register(ArticleComment)

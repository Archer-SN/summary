# Project Description

Summary is a project made for people who don't have much time to read a full book. Summary has book summaries and articles made by users for users to read. Anyone can create their own articles and book summaries on this website. All they need to do is login!

# Distinctiveness and Complexity

1. This project is kind of similar to wiki but it is far more complex than wiki as it has a lot more features than wiki.

2. This project has 6 Django models which are User, Category, Book, Article, BookComment and ArticleComment. 4 of these models are based on one abstract model which is called ContentModel.

3. Javascript is used a lot in this project. It is used to implemenet a sorting system, library system and favorites system.

4. This project is mobile-responsive because it uses bootstrap and media query.

## Files explaination

- ### Templates

    This folder contains all the html used in this project.

    1. card.html is a template for rendering cards. You can use this template by including it in another html file

    2. content.html renders a specific summary or article. The layout of this website varies depending on the type of content you are viewing.
    If you view, an article for example, you will see an image at the top of the page. But if you view a book summary, you won't see any of the image.
    In this page we also have comments you can type your thoughts and read others' thoughts about the content here.

    3. error.html is just an error page. It has a button to redirect you to the index page

    4. form.html handles all the form including creating and editing. The reason this works is because I use Django form.

    5. index.html is the home page. It shows you new books and new articles. Most importantly it shows your library. Your library shows your currently reading books, finished books and
    favorite books.

    6. layout.html just contains a navbar

    7. login.html and register.html are nothing new just registering and logging in.

    8. profile.html shows how many books and articles the user has summarized. It also shows what those books and articles are.
    You can also change your profile picture in this page.

- ### Views

    views.py handles all the backend of this website. This includes logging in, registering, creating summaries, sorting content and more.

- ### Static

    1. content.js handles favoriting and commenting for content.html.

    2. main.js handles all the favoriting, sorting and many others for index.html and list.html.

    3. styles.css contains css that can't be done with bootstrap

## How to run this project

All you need to do is type "python manage.py runserver" and you're good to go!
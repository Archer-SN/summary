# Project Description

Summary is a project made for people who don't have much time to read a full book. Summary has book summaries and articles made by users for users to read. Anyone can create their own articles and book summaries on this website. All they need to do is login!

# Distinctiveness and Complexity

1. This project is kind of similar to wiki but it is far more complex than wiki as it has a lot more features than wiki. In this project we have instant searching system. This system works by typing the name of a book that you want to find and the result will instantly pop up without having to press the search button (Actually we don't have a search button). We also have sorting system. We can sort books and articles based on the date it was created, its popularity and its category. The user can also change their profile picture! Pretty cool!

2. This project has 6 Django models which are User, Category, Book, Article, BookComment and ArticleComment. 4 of these models are based on one abstract model which is called ContentModel.

3. Javascript is used a lot in this project. It is used to implemenet a sorting system, library system and favorites system.

4. This project is mobile-responsive because it uses bootstrap and media query.

## Files explaination

- ### Templates

    This folder contains all the html used in this project.

    1. card.html is a template for rendering cards (card is a div that contains a thumbnail and a title). This is used for both books and articles. When you include this file, you also have to specify the content's type. If you include it in the index page you also have to specify its container type. So that the card can properly display options. I created this file because it is used in so many places.

    2. content.html renders a specific summary or article. The layout of this website varies depending on the type of content you are viewing.
    If you view, an article for example, you will see an image at the top of the page. But if you view a book summary, you won't see any of the image.
    In this page we also have comments you can type your thoughts and read others' thoughts about the content here. You can also favorite a book. The book will pop up in the library. It is in favorites container.

    3. error.html is just an error page. It has a button to redirect you to the index page. I create this page to handle errors that might happen on my website.

    4. form.html is a file for handling forms. It can handle all kinds of forms including creating content and editing content. The reason this works is because I use Django form. The reason I designed the code to only have 1 html to handle forms is because I want to reduce repetition in my program or DRY. 

    5. index.html is the home page. It shows you new books and new articles. Most importantly it shows your library. Your library shows your currently reading books, finished books and favorite books.

    6. layout.html is a base for every single page in this program. Every single html file in this program includes this file. This file contains a navbar. This navbar collapses and grow depending on the user's screen size. If the user is on mobile phone the navbar collapses. If the user is on a pc, the navbar will extend. I created this file to reduce repetition.

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
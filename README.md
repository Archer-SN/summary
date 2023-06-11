# Project Description

Summary is a website made for people who don't have much time to read a full book, but want some wisdom from the book. 
Summary has book summaries and articles made by users for users to read. Anyone can create their own articles and 
book summaries on this website. All they need to do is login!

# Distinctiveness and Complexity

1. This project is kind of similar to wiki but it is far more complex than wiki as it has a lot more features than wiki. In this project we have instant searching system. This system works by typing the name of a book that you want to find and the result will instantly pop up without having to press the search button (Actually we don't have a search button). We also have sorting system. We can sort books and articles based on the date it was created, its popularity and its category. The user can also change their profile picture! Pretty cool! On the index page, we show books and articles that have just been added and we also show the user's library. Library is where user's favorite, currently reading and finished books are. If you click on a book, you will be redirected to the book's content page. On this page you can comment your thoughts on the book.

2. This project has 6 Django models which are User, Category, Book, Article, BookComment and ArticleComment. 4 of these models are based on one abstract model which is called ContentModel.

3. Javascript is used a lot in this project. It is used to implement a sorting system, library system and favorites system.

4. This project is mobile-responsive because it uses bootstrap and media query.

## Files explaination

- ### Templates

    This folder contains all the html used in this project.

    - card.html is a template for rendering cards (card is a div that contains a thumbnail, and a title). This is used for both books and articles. When you include this file, you also have to specify the content's type. If you include it in the index page you also have to specify its container type. So that the card can properly display options. This card also has a favorite system. Each card has a star that the user can click. Clicking this star will favorite a book. The user can unfavorite a book too! They can just click again to unfavorite. Favorite system works in card.html because it is connected to content.js. content.js handles almost all the client-side processes. We'll talk about this file later. The card's background also changes color when being hovered. We accomplished this using css. The reason I created card.html is because card is used in so many files.

    - content.html renders a specific summary or article. The layout of this website varies depending on the type of content you are viewing.
    If you view, an article for example, you will see an image at the top of the page. But if you view a book summary, you won't see any of the image.
    In this page we also have comments you can type your thoughts and read others' thoughts about the content here. You can also favorite a book. The book will pop up in the library. It is in favorites container. 

    - error.html is an error page. error.html extends a layout from layout.html. It has a button to redirect you to the index page. I created this page to handle errors that might happen on my website.

    - form.html is a file for handling forms. It can handle all kinds of forms including creating content and editing content. The reason this works is because I use Django form. The reason I designed the code to only have 1 html to handle forms is because I want to reduce repetition in my program or DRY. 

    - index.html is the home page. It has a code for rendering new books and articles. The data for new books and articles are sent from the server. Only 2 new books and 3 new articles show up on this page. This page also has something called "library". This library shows all sort of things. It shows books you're reading, books you've read and your favorite books. You can move books to favorite, reading and finished. You can also remove books from the library.

    - layout.html is a base for every single page in this program. Every single html file in this program includes this file. This file contains a navbar. This navbar collapses and grow depending on the user's screen size. If the user is on mobile phone the navbar collapses. If the user is on a pc, the navbar will extend. I created this file to reduce repetition. All the javascript and css are imported at the head of this file. layout.html is really necessary in my program becauses it reduces the amount of repetition in my program. With this file, I don't have create a navbar all over again when creating a new file. I can just extend this file. 

    - login.html and register.html are nothing new just registering and logging in.

    - profile.html shows how many books and articles the user has summarized. It also shows what those books and articles are.
    You can also change your profile picture in this page.
      
    - list.html is a page that lists all the books or the articles in the database.

- ### Models
  
  models.py tells the database how to represent data for each class. There are 6 models in here
  - User
  - Category
  - Book
  - Article
  - BookComment
  - ArticleComment

- ### Views

    views.py handles all the backend of this website. This includes logging in, registering, creating summaries, sorting content and more. Here are all the things that are in views.py
    - ProfilePictureForm: Uses django's form template to create a form for profile picture.
    - index: Sends all the necessary data to index.html. These datas include new_books, new_articles, favorite_books, reading_books, finished_books.
    - login_view: Renders login page and handles login system. The user's information is saved in the database.
    - logout_view: Renders logout page and handles logout system. 
    - register_view: Renders register page and handles register system. 
    - book_list: Has 2 functionalities.
      1. Sends JSON response to a request. This response contains the listing of books as specified by the request 
      2. Renders the page that lists all the books.
    - article_list: Similar to book_list but for articles
    - user_view: renders a profile page of a given user
    - book_view: Has 2 functionalities:
      1. Renders the page that contains the book summary's content and comment section.
      2. Handles the request for changing book's status on a user such as favorite, reading, and finished. These are all statuses of the book.
    - article_view: very similar to book_list, but for a webpage.
    - create_book: Uses the data given in the request, create a new entry in the database with the given data. 
      This function also handles rendering a webpage for creating a book summary.
    - create_article: Similar to create_book but for article.
    - edit_book: It handles 2 things, GET and POST. For POST, it modifies the book's data in the database with the data 
      given in the request. For GET, it returns the book's data which is useful for populating the edit page with the book's content.
    - edit_article: Similar to edit_book, but for articles.
    - comment: Handles the request for adding comments to the server
    - error_view: Renders the error page
    - change_profile_picture: Changes the user's profile picture url in the server.
  
- ### Static

    - content.js handles functionalities for content.html. There are 3 functions in this file
        * getCookie: It is used to generate csrfToken for passing token when fetching data from the server.
        * handleFavorite: It is a function that gets called when an event listener for clicking is triggered.
        When the function gets called, it updates the data in the server and also update client's webpage.
          
        * submitComment: it is a function that gets called when an event listener for clicking in a comment button is
        triggered. Again, it sends the comment's data to the server and updates the client's webpage to match the current server data.

    - main.js handles various functionalities for index.html and list.html. It handles the following:
        * getCookie: used for generating csrfToken
        * getContent: Creates "card" of books or articles and render it on the web page.
        * createCard: Creates a "card". This card contains thumbnail, category, title, author, and date created.
        It also has a button for favorites.
          
        * redirect: redirect the user to a new url
        * handleContainers: Creates a book container
        * handleActiveButtons: It just changes the look of showButtons when called.
        * handleFavorite: Handles favorite and unfavorite system on the homepage. For example, when you press favorite
        on a book, it gets added to favoriteContainer. When you, however, unfavorite it, it gets removed.
        * handleReading: Similar to handleFavorite but for books with "reading" status.
        * handleFinished: Similar to handleReading but for books with "finished" status.
        * handleRemove: Handling the removal of books or articles.
        * createDropdown: There is a 3 dot dropdown on a card. This is used to handle additional options that can't be put on the card.
        * addEmptyText: This gets called when there is no data to render on the page.

    - styles.css contains css that can't be done with bootstrap

## How to run this project

All you need to do is type
>python manage.py runserver

, and you're good to go!
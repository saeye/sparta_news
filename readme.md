![header](https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=Sparta%20News)

[![Python Version](https://img.shields.io/badge/Python-3.12.4-3776AB)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2-092E20)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.15.2-FF8C00)](https://www.django-rest-framework.org/)
[![OpenAI Python Client](https://img.shields.io/badge/OpenAI%20Python%20Client-0.28.0-4B92DB)](https://github.com/openai/openai-python)
[![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-4.12.3-8B4C39)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/Requests-2.32.3-FF5B5B)](https://requests.readthedocs.io/)
<br>
[![djangorestframework-simplejwt](https://img.shields.io/badge/djangorestframework--simplejwt-5.3.1-000000)](https://github.com/django-rest-framework-simplejwt/django-rest-framework-simplejwt)
[![Pillow](https://img.shields.io/badge/Pillow-10.4.0-EEAE3F)](https://python-pillow.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.9.1-2E8B57)](https://pydantic.dev/)
[![Psycopg2](https://img.shields.io/badge/Psycopg2-2.9.9-8A2B2C)](https://www.psycopg.org/)

<br>

## 📖 Navigation

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [API Documentation](#api-documentation)
5. [Wireframe]((#wireframe))
6. [ERD](#erd)
7. [Role Distribution](#role-distribution)
8. [Demo Video](#demo-video)

<br>

## Introduction

This project is designed to build an API server using Django Rest Framework (DRF). It provides a backend solution for managing news articles, comments, user accounts, and various interactive features. The API server allows developers to create and customize news-related applications efficiently.

You can access the live demo of the project [here](배포시 링크 추가예정).


### Duration
24.09.11 - 24.09.19
<br><br>

## Features
- **User Authentication:** Users can sign up, log in, and manage their profiles with different permission levels.
- **Articles Management:** Users can create, view, update, and delete news articles. Posts are available for authenticated users, and administrators can manage categories.
- **Comment System:** Users can add, view, update, and delete comments on news articles. Notifications are sent to the article author when a new comment is added.
- **Likes System:** Users can like and unlike news articles. Points are awarded to the article author when their article is liked.
- **Search Functionality:** Search news articles based on various criteria such as title, content, or author. Integrated support for searching across multiple fields.
- **User Liked News:** Users can view a list of news articles they have liked.
- **Web Crawling:** Allows authenticated users to crawl external news websites, extract articles, and save them to the database. Supports multiple news sources with specific parsers.
- **Dynamic News Summarization:** Automatically summarizes the content of news articles into concise, digestible chunks.
- **Multilingual Translation:** Translates news summaries into Korean for English content.
- **Points System:** Users earn points for creating posts, receiving likes, and writing comments. Points can be tracked and incentivize user engagement.
- **Email Notifications:** Authors receive email notifications when new comments are made on their posts.

<br><br>
  
## installation
To set up and run the project, follow these steps:

1. Clone the project repository:

    ```bash
    git clone https://github.com/saeye/sparta_news.git
    ```

2. Navigate to the project directory:

    ```bash
    cd /Users/YourPC/Your_Cloned_Folder/
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create and configure the `config.py` file:**

    Create a file named `config.py` in the project root directory and add the following content:

    ```python
    # config.py

    DJANGO_SECRET_KEY = "your_django_secret_key_here"

    OPENAI_API_KEY = "your_openai_api_key_here"

    # for sending emails from the Django application
    EMAIL_ADDRESS = 'your_email_address_here'
    EMAIL_HOST_PASSWORD = 'your_email_app_password_here'
    ```

5. **Apply database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Open your browser and visit:**

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
<br><br><br>


## Wireframe

![image](https://github.com/user-attachments/assets/b125f238-559f-4826-8820-c2d2a046a98c)


<br><br>


## API Documentation

### User Management

| **Endpoint**                       | **Method** | **Description**                       | **Parameters**                                                                 | **Permissions**          |
|------------------------------------|------------|---------------------------------------|--------------------------------------------------------------------------------|--------------------------|
| `/api/users/`                      | GET        | Retrieve list of users                | -                                                                              | `IsAuthenticated`        |
| `/api/users/profile/<int:user_id>/` | GET        | Retrieve user profile                 | `user_id` (required): User ID                                                   | `IsAuthenticated`        |
| `/api/users/profile/update/`       | PUT        | Update user profile                  | -                                                                              | `IsAuthenticated`        |
| `/api/users/signup/`               | POST       | User signup                           | `username` (required) <br> `password` (required) <br> `email` (required)        | -                        |
| `/api/users/signin/`               | POST       | User login                            | `username` (required) <br> `password` (required)                               | -                        |
| `/api/users/signout/`              | POST       | User logout                           | -                                                                              | `IsAuthenticated`        |
| `/api/users/follow/<int:user_id>/` | POST       | Follow a user                         | `user_id` (required): User ID to follow                                        | `IsAuthenticated`        |
| `/api/users/changepassword/`       | PUT        | Change password                       | `current_password` (required) <br> `new_password` (required)                    | `IsAuthenticated`        |
| `/api/users/deleteuser/`           | DELETE     | Delete user                           | -                                                                              | `IsAuthenticated`        |
| `/api/users/email/confirmation/<str:passkey>` | GET | Email confirmation                    | `passkey` (required): Passkey for email confirmation                           | -                        |


### News Management

| **Endpoint**                        | **Method** | **Description**                        | **Parameters**                                                                 | **Permissions**          |
|-------------------------------------|------------|----------------------------------------|--------------------------------------------------------------------------------|--------------------------|
| `/api/news/`                        | GET        | Retrieve list of news items            | -                                                                              | `IsAuthenticated`        |
| `/api/news/create/`                 | POST       | Create a news post                     | `title` (required) <br> `content` (required) <br> `category` (optional)          | `IsAuthenticated`        |
| `/api/news/<int:pk>/`               | GET        | Retrieve news post details             | `pk` (required): News ID                                                        | `IsAuthenticated`        |
| `/api/news/<int:pk>/`               | PUT        | Update a news post                     | `pk` (required): News ID <br> `title` (optional) <br> `content` (optional)       | `IsAuthenticated`        |
| `/api/news/<int:pk>/`               | DELETE     | Delete a news post                     | `pk` (required): News ID                                                        | `IsAuthenticated`        |
| `/api/news/category/`               | POST       | Create a news category                 | `name` (required)                                                                | `IsAuthenticated`        |
| `/api/news/like/<int:pk>/`          | POST       | Like/Unlike a news post                | `pk` (required): News ID                                                        | `IsAuthenticated`        |
| `/api/news/user/liked/`             | GET        | Retrieve news liked by the user        | -                                                                              | `IsAuthenticated`        |
| `/api/news/news_crawling/`          | POST       | Crawl news content,<br> proccess with LLM, <br> to create a news post               | `url` (required): News article URL <br> `category` (optional)                   | `IsAuthenticated`        |

### Comment Management

| **Endpoint**                      | **Method** | **Description**                         | **Parameters**                                                                 | **Permissions**          |
|-----------------------------------|------------|-----------------------------------------|--------------------------------------------------------------------------------|--------------------------|
| `/api/news/<int:news_pk>/comments/` | GET        | Retrieve comments for a news article    | `news_pk` (required): News article ID                                           | `IsAuthenticated`        |
| `/api/news/<int:news_pk>/comments/` | POST       | Post a comment                          | `news_pk` (required): News article ID <br> `content` (required) <br> *2 points awarded upon success* | `IsAuthenticated`        |
| `/api/comments/<int:comment_pk>/`   | PUT        | Update a comment                        | `comment_pk` (required): Comment ID <br> `content` (required)                   | `IsAuthenticated`        |
| `/api/comments/delete/<int:comment_pk>/` | DELETE     | Delete a comment                        | `comment_pk` (required): Comment ID                                               | `IsAuthenticated`        |



<br>
For more details, refer to our documentation <br>

***[📖 API documentation](https://documenter.getpostman.com/view/37996824/2sAXqs62Yd)*** <br>
***[📚 SA documentation](https://www.notion.so/teamsparta/DRF-SA-d792a0eaa0844c8b890b011a95d1e841)*** <br>
***[🙌 Team Notion Page](https://www.notion.so/teamsparta/30ea3dd32eb4490c9434d821caf38057)***

<br><br>

## ERD

<img width="1083" alt="스크린샷 2024-09-19 오후 6 14 23" src="https://github.com/user-attachments/assets/45c0b12e-e51d-4c7a-86db-3f87eb63ed0c">

<br><br>

## Role Distribution

| **Name**                           | **GitHub Handle**                                                   | **Responsibilities**                                                                                           |
|------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Saeye Lee**                      | [@saeye](https://github.com/saeye)                                  | User registration, password reset, profile update, account deletion, and point system implementation.           |
| **Woolin Kim**                    | [@kimwoolina](https://github.com/kimwoolina)                        | Comment creation, retrieval, update, deletion, login, logout, article summarization and translation using GPT API |
| **Jisu Na**                        | [@qwerrrqw](https://github.com/qwerrrqw)                            | Post creation, post listing, category management, search functionality, and web crawling.                        |
| **Sejun Lee**                      | [@gr22nsky](https://github.com/gr22nsky)                            | Follow/unfollow, profile viewing, comment notification, and user update throttling.                              |
| **Minseong Jeon**                  | [@Oztalun](https://github.com/Oztalun)                              | Post editing, deletion, viewing, and email verification implementation.                                         |

<br>

## Demo Video
시연영상 첨부예정.

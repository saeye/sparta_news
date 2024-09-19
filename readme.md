![header](https://capsule-render.vercel.app/api?type=waving&height=300&color=gradient&text=Spart%20News)

[![Python Version](https://img.shields.io/badge/Python-3.12.4-3776AB)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2-092E20)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.15.2-FF8C00)](https://www.django-rest-framework.org/)
[![OpenAI Python Client](https://img.shields.io/badge/OpenAI%20Python%20Client-0.28.0-4B92DB)](https://github.com/openai/openai-python)
[![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-4.12.3-8B4C39)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/Requests-2.32.3-FF5B5B)](https://requests.readthedocs.io/)
[![Pillow](https://img.shields.io/badge/Pillow-10.4.0-EEAE3F)](https://python-pillow.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.9.1-2E8B57)](https://pydantic.dev/)
[![Psycopg2](https://img.shields.io/badge/Psycopg2-2.9.9-8A2B2C)](https://www.psycopg.org/)

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

This project is designed to build a comprehensive news API server using Django Rest Framework (DRF). It provides a robust backend solution for managing news articles, comments, user accounts, and various interactive features. The API server allows developers to create and customize news-related applications efficiently.

### Duration
24.09.11 - 24.09.19
<br><br>

## Features
- **User Authentication:** Users can sign up, log in, and manage their profiles with different permission levels.
- **Articles Management:** Users can create, view, update, and delete news articles. Posts are available for authenticated users, and administrators can manage categories.
- **Comment System:** Users can add, view, update, and delete comments on news articles. Notifications are sent to the article author when a new comment is added.
- **Likes System:** Users can like and unlike news articles. Points are awarded to the article author when their article is liked.
- **Search Functionality:** Search news articles based on various criteria such as title, content, or author. Integrated support for searching across multiple fields.
- **Sorting and Ranking:** News articles can be sorted and ranked based on various metrics including recency and user engagement (likes, comments).
- **User Liked News:** Users can view a list of news articles they have liked.
- **Web Crawling:** Allows authenticated users to crawl external news websites, extract articles, and save them to the database. Supports multiple news sources with specific parsers.
- **Dynamic News Summarization:** Automatically summarizes the content of news articles into concise, digestible chunks.
- **Multilingual Translation:** Translates news summaries into multiple languages for broader accessibility.
- **Points System:** Users earn points for creating posts, receiving likes, and writing comments. Points can be tracked and incentivize user engagement.
- **Email Notifications:** Authors receive email notifications when new comments are made on their posts.


  
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
이미지 첨부예정.
<br>


## API Documentation

### 회원 (User)



| **Endpoint**             | **Method** | **Description**     | **Parameters**                                                                 |
|--------------------      |------------|-------------------- |--------------------------------------------------------------------------------|
| `signup/`                | POST       | 회원 가입         | `username`, `password`, `email`               |
| `signin/`                | POST       | 로그인           | `username`, `password`|
| `signout/`               | POST       | 로그아웃          |refresh_token                                                                                |
| `profile/<int:user_id>/` | PUT        | 회원 정보 조회     | 'username', `email`, 'intro', 'profile_image', 'point' |
| `profile/update/`        | PUT        | 회원 정보 수정     | `intro`, `email`, 'profile_image' |
| `changepassword/`        | PUT        | 비밀번호 변경      | `current_password`, `new_password`                      |
| `deleteuser/`            | PUT        | 회원탈퇴          | `access token`                      |


<br>

### 게시글 목록 조회 및 관리

| **Endpoint**         | **Method** | **Description**        | **Parameters**                                                                 |
|----------------------|------------|------------------------|--------------------------------------------------------------------------------|
| ""                   | GET        | 뉴스 목록 조회          | Returns: `title`, `link`, `summary`, `votes`, `author`, `time`, `comments_count` |
| `/news/create`       | POST       | 뉴스 등록               | `title` (required), `link` (required), `category` (optional), `content` (optional) |
| `/news/search`       | GET        | 뉴스 리스트 페이지 조회  | Query: `search_term` <br> Returns: `title`, `link`, `summary`, `likes`, `author`, `time`, `comments_count`, `likes_count` |
| `/news/detail/{id}`  | GET        | 뉴스 상세 페이지        |                   |
| `/news/update/{id}`  | PUT        | 뉴스 수정               | `title` (optional), `link` (optional), `category` (optional), `content` (optional) |
| `/news/delete/{id}`  | DELETE     | 뉴스 삭제               |

<br>

### 댓글 관리

| **Endpoint**            | **Method**  | **Description**    | **Parameters**                                                                 |
|-------------------------|-------------|--------------------|--------------------------------------------------------------------------------|
| `/comments/list/{newsId}`| GET         | 댓글 조회           | Returns: List of comments with fields: `content`, `author`, and `time`.         |
| `/comments/add/{newsId}`| POST        | 댓글 등록           | `content` (required) <br> *On success, 2 points are awarded.*                  |
| `/comments/delete/{id}`  | DELETE      | 댓글 삭제           |

<br>

### 좋아요 기능

| **Endpoint**       | **Method**  | **Description**    | **Parameters**                                                                 |
|--------------------|-------------|--------------------|--------------------------------------------------------------------------------|
| `/like/news/{id}`  | POST        | 뉴스 좋아요         | *On success, 1 or point is awarded to the user who liked the news.*              |

<br>
For more details, refer to our [API documentation](API문서첨부예정).
<br><br>

## ERD
이미지 첨부예정.
<br>

## Role Distribution

| **Name**                           | **GitHub Handle**                                                   | **Responsibilities**                                                                                           |
|------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Saeye Lee**                      | [@saeye](https://github.com/saeye)                                  | User registration, password reset, profile update, account deletion, and point system implementation.           |
| **Woolina Kim**                    | [@kimwoolina](https://github.com/kimwoolina)                        | Comment creation, modification, retrieval, deletion, login, logout, article summarization and translation using GPT API, and post creation. |
| **Jisu Na**                        | [@qwerrrqw](https://github.com/qwerrrqw)                            | Post creation, post listing, category management, search functionality, and web crawling.                        |
| **Sejun Lee**                      | [@gr22nsky](https://github.com/gr22nsky)                            | Follow/unfollow, profile viewing, comment notification, and user update throttling.                              |
| **Minseong Jeon**                  | [@Oztalun](https://github.com/Oztalun)                              | Post editing, deletion, viewing, and email verification implementation.                                         |

<br>

## Demo Video
시연영상 첨부예정.

## 회원 (User)
<br>

| **Endpoint**             | **Method** | **Description**     | **Parameters**                                                                 |
|--------------------      |------------|-------------------- |--------------------------------------------------------------------------------|
| "signup/"                | POST       | 회원 가입         | `username` (required), `password` (required), `email` (required)               |
| "signin/"                | POST       | 로그인           | `username` (required), `password` (required) <br> *On success, 1 point is awarded.* |
| "signout/"               | POST       | 로그아웃          |refresh_token                                                                                |
| "profile/<int:user_id>/" | PUT        | 회원 정보 조회     | `introduction` (optional), `email` (optional) <br> *Username and points are visible but not editable. Password can be changed separately.* |
| "profile/update/"        | PUT        | 회원 정보 수정     | `introduction` (optional), `email` (optional) <br> *Username and points are visible but not editable. Password can be changed separately.* |
| "changepassword/".       | PUT        | 비밀번호 변경      | `current_password` (required), `new_password` (required)                       |
| "deleteuser/".           | PUT        | 비밀번호 변경      | `current_password` (required), `new_password` (required)                       |

<br>

## 게시판 (Board)<br>
<br>

### 뉴스 목록 조회 및 관리

| **Endpoint**         | **Method** | **Description**        | **Parameters**                                                                 |
|----------------------|------------|------------------------|--------------------------------------------------------------------------------|
| ""                   | GET        | 뉴스 목록 조회          | Returns: `title`, `link`, `summary`, `votes`, `author`, `time`, `comments_count` |
| `/news/create`       | POST       | 뉴스 등록               | `title` (required), `link` (required), `category` (optional), `content` (optional) |
| `/news/search`       | GET        | 뉴스 리스트 페이지 조회  | Query: `search_term` <br> Returns: `title`, `link`, `summary`, `likes`, `author`, `time`, `comments_count`, `likes_count` |
| `/news/detail/{id}`  | GET        | 뉴스 상세 페이지        | Returns: `title`, `link`, `content`, `author`, comments list                    |
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
| `/like/news/{id}`  | POST        | 뉴스 좋아요         | *On success, 1 point is awarded to the user who liked the news.*              |

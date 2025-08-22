# Social Media API

A Django REST Framework-based API for user authentication and profile management.

## Features
- Custom User Model (with bio, profile picture, followers)
- Token Authentication
- Endpoints: Register, Login, Profile

## Setup
```bash
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



## Posts & Comments API

Base: `/api/`

### Posts
- `GET /api/posts/` — list posts (supports `?search=`, `?page=`, `?page_size=`, ordering)
- `POST /api/posts/` — create (auth required)
  - body: `{ "title": "string", "content": "string" }`
- `GET /api/posts/{id}/` — retrieve
- `PATCH /api/posts/{id}/` — partial update (owner only)
- `DELETE /api/posts/{id}/` — delete (owner only)

### Comments
- `GET /api/comments/` — list (supports `?post=`, filtering)
- `POST /api/comments/` — create (auth required)
  - body: `{ "post": <post_id>, "content": "string" }`
- `PATCH /api/comments/{id}/` — partial update (owner only)
- `DELETE /api/comments/{id}/` — delete (owner only)

Authorization: `Authorization: Token <token>`

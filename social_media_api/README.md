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

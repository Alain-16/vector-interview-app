# Vector Interview App

Vector Interview is an asynchronous video interview platform designed to streamline the hiring process. Recruiters can pre-record questions and candidates respond at their convenience, while evaluators perform blind reviews. This repository contains the backend built with Django and Django REST Framework (DRF) along with JWT-based authentication and a custom HTML interface for signup and login.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Usage](#usage)
  - [HTML Interface](#html-interface)
  - [REST API](#rest-api)
- [Deployment](#deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

Vector Interview simplifies the interview scheduling process, improves hiring efficiency, and ensures unbiased candidate evaluations by providing:

- Pre-recorded interview questions.
- Asynchronous candidate video responses.
- Blind review of submissions by evaluators.
- Automated candidate scoring and report generation.

## Features

- **JWT Authentication:** Implements JSON Web Token (JWT) based signup and login.
- **REST API Endpoints:**
  - Endpoints for signup and login with appropriate redirections and messages.
  - Endpoints for creating an interview session
- **Docker Deployment:** (Optional) Containerized deployment using Docker and Docker Compose.

## Architecture

- **Backend:** Django with Django REST Framework.
- **Authentication:** JWT tokens using [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt).

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (or another supported database)
- pip (or a virtual environment manager)
- (Optional) Docker and Docker Compose for containerized deployment

### Local Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Alain-16/vector-interview-app.git
    cd vector-interview-app
    ```

    a. **Create and activate a virtual environment:**

          python3 -m venv my_env
          source my_env/bin/activate

B. **Install Dependencies:**

    pip install -r requirements.txt

    "Ensure your requirements.txt includes:
        Django
        djangorestframework
        djangorestframework-simplejwt
        psycopg2-binary (for PostgreSQL)
        django-environ (optional, for environment variables)"

C. **Edit your settings.py to configure:**

Database Configuration:

    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'vector_interview_db',
    'USER': 'your_db_user',
    'PASSWORD': 'your_db_password',
    'HOST': 'localhost',
    'PORT': '5432',
    }
    }

D. **Database Migrations:**

    After configuring your database run:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

If you encounter issues with migration history (especially with custom user models), you may need to clear cached migrations (development only).
Usage
HTML Interface

# Testing for JWT Signup and Login base authentication

The app provides HTML views for signup and login:

    Signup Page: Accessible at http://localhost:8000/api/vector-interview/signup/
    Login Page: Accessible at http://localhost:8000/api/vector-interview/login/

These pages use custom templates located in templates/ (e.g., signup.html, login.html).

2. **REST API Testing for JWT signup and login based authentication:**

For API testing, you can send JSON requests to the endpoints:

Signup:

    curl -X POST http://localhost:8000/api/vector-interview/signup/ \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"username": "newuser", "email": "newuser@example.com", "password": "newpass123", "password2": "newpass123", "action": "signup"}'

Login:

    curl -X POST http://localhost:8000/api/vector-interview/login/ \
         -H "Content-Type: application/json" \
         -H "Accept: application/json" \
         -d '{"username": "newuser", "password": "newpass123", "action": "login"}'

**API RESPONSES:**

    {
    "detail": "Logged in successfully",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNzM5OTE2LCJpYXQiOjE3NDE3MzkwMTYsImp0aSI6IjMzMWVhYTBkNWY3YzRiMzliMjkwMTNlYmMwYmNmMWFkIiwidXNlcl9pZCI6MX0.m7Xa6NDYBUgrCFna8F0HRyQt5nqlTsnWUSqDdcb9Ia0",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTgyNTQxNiwiaWF0IjoxNzQxNzM5MDE2LCJqdGkiOiJkNjJjMzE4YWY0MTI0ZTVhODM0NzM1NWZhNzI5ZjQ5NSIsInVzZXJfaWQiOjF9.9BlKCnavEdp1rK1ckwNwclGn5gAa2FcOCzC9h4TiR4o"
    }

JSON requests will return a response with JWT tokens (access and refresh).

# TESTING APIs FOR CREATING INTERVIEW SESSION

The API for creating an interview session allows users to create set an interview with questions, it is designed in a way that each interview record has its corresponding questions associated with it.

1.  **Create interview session:**

        curl -X POST http://127.0.0.1:8000/api/interviews/create/ \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Software Engineer Interview",
            "description": "First-round technical interview",
            "questions": [
                {"question_text": "What is your experience with Django?"},
                {"question_text": "How do you optimize database queries?"}
            ]
        }'

2.  **API Response:**

        {
            "id":1,
            "title":"Software Engineer interview",
            "description":"First-round technical interview"
        }

# REST API FOR FETCHING ALL INTERVIEWS AND GET INTERVIEW DETAIL BY ID WHILE APPLYING PAGINATION

1.  **REST API for fetching all interviews:**

        curl -X GET http://localhost:8000/api/interviews/interview?page_size=5 \
        -H "Content-Type: application/json"

2.  **REST API for getting interview details using ID:**

        curl -X GET http://localhost:8000/api/interviews/interview/<int:pk>?page_size=5 \
        -H "Content-Type: application/json"

# REST API FOR UPLOADING VIDEO USING AWS S3

1.  **REST API for uploading the video:**

            curl -X POST http://localhost:8000/api/interviews/upload-video \
        -H "Content-Type: multipart/form-data" |

    Body-format(key:value):

        video_title:"your-value"
        video_file:"your-file path"

2.  **API Response:**

        {
        "id": 13,
        "video_title": "trial video",
        "video_file": "/simplescreenrecorder-2024-05-15_01_k03ONyi.06.40.mp4",
        "video_url": "/simplescreenrecorder-2024-05-15_01_k03ONyi.06.40.mp4",
        "duration": 15.86,
        "uploaded_at": "2025-03-19T07:54:35.493969Z"

    }

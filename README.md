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

- **Custom User Model:** Extends Django's default user model to include roles (candidate, recruiter, evaluator, HR), phone number, company, and more.
- **JWT Authentication:** Implements JSON Web Token (JWT) based signup and login.
- **Dual Interface:** Supports both HTML-based views (for browsers) and JSON responses (for API testing via Postman or curl).
- **Docker Deployment:** (Optional) Containerized deployment using Docker and Docker Compose.
- **Production-ready Settings:** Environment variables, secure settings, and logging configurations.
- **REST API Endpoints:** Endpoints for signup and login with appropriate redirections and messages.

## Architecture

- **Backend:** Django with Django REST Framework.
- **Authentication:** JWT tokens using [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt).
- **Custom User Model:** Located in `vector_interview_app/models.py` as `VectorUser`.
- **Views:** Dual-rendered API views using DRF’s `TemplateHTMLRenderer` and `JSONRenderer` for both HTML and JSON responses.
- **Forms and Templates:** HTML forms for signup and login reside in the `templates/` directory.

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (or another supported database)
- pip (or a virtual environment manager)
- (Optional) Docker and Docker Compose for containerized deployment

### Local Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Alain-16/vector-interview-app.git
   cd vector-interview-app
   Setup configuration
   ```

python3 -m venv my_env
source my_env/bin/activate

Install Dependencies:

    pip install -r requirements.txt

    Ensure your requirements.txt includes:
        Django
        djangorestframework
        djangorestframework-simplejwt
        psycopg2-binary (for PostgreSQL)
        django-environ (optional, for environment variables)

Configuration

Edit your settings.py to configure:

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

Database Migrations

After configuring your database run:

python manage.py makemigrations
python manage.py migrate

If you encounter issues with migration history (especially with custom user models), you may need to clear cached migrations (development only).
Usage
HTML Interface

The app provides HTML views for signup and login:

    Signup Page: Accessible at http://localhost:8000/auth/signup/
    Login Page: Accessible at http://localhost:8000/auth/login/

These pages use custom templates located in templates/ (e.g., signup.html, login.html).

REST API

For API testing, you can send JSON requests to the endpoints:

Signup:

    curl -X POST http://localhost:8000/auth/signup/ \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"username": "newuser", "email": "newuser@example.com", "password": "newpass123", "password2": "newpass123", "action": "signup"}'

Login:

    curl -X POST http://localhost:8000/auth/login/ \
         -H "Content-Type: application/json" \
         -H "Accept: application/json" \
         -d '{"username": "newuser", "password": "newpass123", "action": "login"}'

JSON requests will return a response with JWT tokens (access and refresh).

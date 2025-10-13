# Study Nest

A personal project to manage / deliver study content (courses, lessons, media, notifications, reviews) — built with Python / Django Rest Framework.

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Running the Application](#running-the-application)  
- [Project Structure](#project-structure)  

---

## About

**study nest** is a Django-based personal project providing a backend and API for educational content similar to Udemy.

## Features
  
- Models with Django ORM
- Improved Admin Panel
- Django Restful APIs with Model ViewSet (filter, search, ordering provided)
- Authentication with JWT
- APIs with permissions (rules of Admin, Instructor, Student)
- Swagger and documentation
- Caching and Celery with Redis
- Notifications with celery beat
- Media / Static files handing
- Home Page, Loggers, Test cases
- PostgreSQL database

## Getting Started

### Prerequisites

- Python 3.12.10
- pip / pipenv / virtualenv  
- PostgreSQL
- Redis
- Celery (doesn't work in Windows and need WSL)
- Pip packages in Pipfile

### Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/FaranF/study-nest.git
   cd study-nest
   ```

2. Connect PostgreSQL database  
   You can use SQL dump file `study_nest.sql`
   You can also use your own database and fill it with the following command:
   ```bash
   python manage.py generate_dummy_data
   ```

3. Create & activate virtual environment  
   ```bash
   pipenv install #installs project dependencies
   pipenv shell
   ```

### Running the Application

4. Run the Migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the Server:
   ```bash
   python manage.py runserver #defualt at 'http://127.0.0.1:8000/'
   ```

6. Create superuser (for admin access)  
   ```bash
   python manage.py createsuperuser
   ```

7. For Celery tasks / Celery beat, start worker / beat as needed:
   ```bash
   celery -A study_nest worker --loglevel=info
   celery -A study_nest beat --loglevel=info
   ```

## Project Structure

Each app (core, course, notification, review) encapsulates a domain of functionality.

- `core`: shared utilities, profile and user authentications
- `course`: courses, lessons, categories, enrollments, progresses 
- `notification`: notification with celery beats
- `review`: simple review app with ContentType and GenericForeignKey


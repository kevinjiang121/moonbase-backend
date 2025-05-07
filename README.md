# Moonbase Backend

A Django 5.1 + Channels backend providing REST APIs and WebSocket support for the Moonbase chat platform.

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Getting Started](#getting-started)  
   - [Clone & Install](#clone--install)  
   - [Environment Configuration](#environment-configuration)  
   - [Database Migrations](#database-migrations)  
   - [Development Server](#development-server)  
5. [Building for Production](#building-for-production)  
6. [Testing](#testing)  
   - [Unit & Integration Tests](#unit--integration-tests)  
7. [Docker](#docker)  
8. [Project Structure](#project-structure)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Project Overview

The backend for "Moonbase", a real‑time chat and community plaform, with:

- **REST** APIs for signup, login, password reset, channels & chats  
- **JWT**‑based authentication  
- **WebSocket** messaging via Django Channels  
- PostgreSQL for data storage and Redis for channel layers  

---

## Features

- **Authentication**: signup, login, forgot/reset password  
- **Channels** & **Channel Groups** CRUD  
- **Chats** stored via REST and live broadcast over WebSockets  
- **Password Reset** using signed tokens  
- Configurable **EMAIL_BACKEND** for console/file/SMTP  
- Docker Compose for easy local development  

---

## Prerequisites

- Python 3.9+  
- PostgreSQL  
- Redis  
- Docker & Docker Compose (optional)  

---

## Getting Started

### Clone & Install

```bash
git clone https://github.com/kevinjiang121/moonbase-backend.git
cd moonbase-backend
```

### Environment Configuration

Create a `.env` file in project root:

```
# Database
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

# Django
SECRET_KEY
DEBUG

# Frontend Urls
FRONTEND_URL_DEV
```

### Database Migrations

```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```

### Development Server
```
# Using local Python environment
python manage.py runserver 0.0.0.0:8000

# Or with Docker Compose
docker-compose up --build web
```

The API will be available at `http://localhost:8000`.

# Building for Production

- Ensure DEBUG=False and proper ALLOWED_HOSTS in settings.py.
- Use a production‑grade WSGI/ASGI server (e.g., Uvicorn/Gunicorn).
- Collect static files if serving via Django:

```
python manage.py collectstatic
```

# Testing

## Unit & Integration Tests

```
# Local
python manage.py test

# With Docker
docker-compose run web python manage.py test
```

Covers REST endpoints and WebSocket consumer behavior.

# Docker

```
# Build and start services
docker-compose up --build

# View backend logs
docker-compose logs -f web
```

Services defined in `docker-compose.yml`:
- **db**: Postgres
- **redis**: Redis
- **web**: Django + Daphne ASGI server

# Project Structure
```
kevinjiang121-moonbase-backend/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .dockerignore
└── moonbase_backend/
    ├── manage.py
    ├── moonbase_backend/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── apps/
        ├── auth/
        ├── users/
        ├── channels/
        └── chats/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

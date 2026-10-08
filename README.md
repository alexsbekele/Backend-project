![CI](https://github.com/alexsbekele/Backend-project/actions/workflows/ci.yml/badge.svg)

# Task API

A REST API for managing personal tasks, built with FastAPI and PostgreSQL.

## Features

- User registration and login with bcrypt-hashed passwords
- JWT authentication
- Per-user authorization: users can only see and modify their own tasks
- Full CRUD for tasks
- Alembic database migrations
- Automated tests with pytest
- Docker Compose setup

## Tech stack

FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, PyJWT, pytest, Docker

## Run with Docker

1. Create a `.env` file:

JWT_SECRET=replace_with_a_long_random_string


   Generate one with:
   `python -c "import secrets; print(secrets.token_hex(32))"`

2. Start everything:

docker compose up --build


3. Open http://127.0.0.1:8000/docs

## Run locally

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Create a `.env` with `JWT_SECRET` and `DATABASE_URL`, then:

alembic upgrade head
uvicorn main:app --reload


## Run the tests

pytest -v


Tests use an in-memory SQLite database and don't touch your real data.

## API overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Create an account |
| POST | /auth/login | No | Get a JWT |
| GET | /users/me | Yes | Current user |
| GET | /tasks | Yes | List your tasks |
| POST | /tasks | Yes | Create a task |
| GET | /tasks/{id} | Yes | Get one task |
| PUT | /tasks/{id} | Yes | Update a task |
| DELETE | /tasks/{id} | Yes | Delete a task |

## Project structure
# Task Management API

A RESTful API for managing personal tasks, built with FastAPI and SQLAlchemy.

## Features
- User registration and authentication (JWT)
- Password hashing with bcrypt
- Full CRUD operations for tasks
- Each user can only access their own tasks

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib + bcrypt

## Setup
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with `SECRET_KEY=your_secret_key`
5. Run the server: `uvicorn main:app --reload`
6. Visit `/docs` for interactive API documentation

## Endpoints
- `POST /register/` - Register a new user
- `POST /login/` - Login and get access token
- `GET /tasks/` - Get all tasks for current user
- `POST /tasks/` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
## What I Learned
Building this project, I learned how JWT authentication works end-to-end, 
and debugged real issues like SQLite schema mismatches and bcrypt version conflicts.
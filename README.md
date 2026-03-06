# FastAPI + MySQL Docker Example

## Overview

This project demonstrates how to run a FastAPI application connected to a MySQL database using Docker and SQLAlchemy.

The application runs inside a Docker container and communicates with a MySQL database container through Docker Compose. It shows a simple example of building a containerized backend service.

---

## Tech Stack

* FastAPI
* SQLAlchemy
* MySQL 8
* Docker
* Docker Compose

---

## Architecture

```
Client (Browser / API Client)
            │
            ▼
      FastAPI Container
            │
            ▼
       MySQL Container
```

The FastAPI container connects to the MySQL container using Docker's internal network.

---

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
└── database.py
```

---

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/your-repo/fastapi-mysql-docker.git
cd fastapi-mysql-docker
```

### 2. Build and Start Containers

```
docker compose up --build
```

### 3. Access the API

Open your browser and go to:

```
http://localhost
```

---

## API Endpoint

### Get Users

```
GET /
```

Returns all users stored in the database.

Example response:

```
{
  "result": [
    {
      "id": 1,
      "name": "Alice"
    },
    {
      "id": 2,
      "name": "Bob"
    }
  ]
}
```

---

## Database Configuration

The MySQL container is configured with the following environment variables:

```
MYSQL_ROOT_PASSWORD=1234
MYSQL_DATABASE=oz
```

Connection information used by the API:

```
mysql+pymysql://root:1234@db:3306/oz
```

---

## Dependencies

The project uses the following Python packages:

```
fastapi
sqlalchemy
pymysql
cryptography
```

All dependencies are defined in `requirements.txt`.

---

## Development Notes

The database connection is handled using SQLAlchemy's `sessionmaker` to create database sessions for each request.

Example:

```
with SessionFactory() as session:
    stmt = text("SELECT * FROM users")
    result = session.execute(stmt).mappings().all()
```

---

## Future Improvements

Possible extensions to this project include:

* Implementing SQLAlchemy ORM models
* Adding CRUD APIs
* Introducing environment variables with `.env`
* Database migrations using Alembic
* Adding health check endpoints
* Separating API routes into modules


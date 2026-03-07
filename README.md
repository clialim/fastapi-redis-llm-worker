# FastAPI + MySQL + Redis Worker (Docker)

Containerized backend example with FastAPI, MySQL, Redis, and background workers using Docker Compose.

## Overview

This project demonstrates how to build a containerized backend system using **FastAPI**, **MySQL**, and **Redis** with **Docker Compose**.

The architecture separates the application into two services:

* **API service** – Handles HTTP requests and database operations
* **Worker service** – Processes background jobs using Redis

This structure reflects a common backend pattern used in production systems where long-running tasks are processed asynchronously.

---

## Tech Stack

* FastAPI
* SQLAlchemy
* MySQL 8
* Redis
* Docker
* Docker Compose

---

## Architecture

```text
Client (Browser / API Client)
            │
            ▼
       FastAPI (API)
            │
            ├───────────────► MySQL
            │
            ▼
           Redis
            │
            ▼
          Worker
```

**Flow**

1. Client sends a request to the FastAPI server
2. FastAPI reads/writes data from MySQL
3. Tasks can be pushed to Redis
4. Worker consumes tasks from Redis and processes them

---

## Project Structure

```text
.
├── api
│   ├── Dockerfile
│   ├── main.py
│   ├── database.py
│   └── requirements.txt
│
├── worker
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Services

### API

FastAPI server that:

* handles HTTP requests
* connects to MySQL using SQLAlchemy
* may push tasks to Redis

### Worker

Background service that:

* listens to Redis queues
* processes asynchronous jobs

---

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/clialim/fastapi-mysql-docker.git
cd fastapi-mysql-docker
```

### 2. Build and Start Containers

```
docker compose up --build
```

### 3. Access the API

Open your browser:

```
http://localhost
```

---

## API Endpoint

### Get Users

```
GET /
```

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

MySQL container configuration:

```
MYSQL_ROOT_PASSWORD=1234
MYSQL_DATABASE=oz
```

Connection string used in the API:

```
mysql+pymysql://root:1234@db:3306/oz
```

---

## Redis Worker Example

The worker connects to Redis and continuously checks for tasks.

Example pattern:

```
while True:
    job = redis_client.lpop("job_queue")

    if job:
        process(job)
```

This pattern enables **asynchronous task processing** outside the API request lifecycle.

---

## Development Notes

* The API uses **SQLAlchemy sessionmaker** to manage database sessions.
* Each request creates its own database session.
* Redis enables decoupling between API and background workers.

Example database session:

```
with SessionFactory() as session:
    stmt = text("SELECT * FROM users")
    result = session.execute(stmt).mappings().all()
```

---

## Future Improvements

Possible extensions:

* Implement SQLAlchemy ORM models
* Add full CRUD APIs
* Introduce `.env` configuration
* Add Redis task queue examples
* Add database migrations with Alembic
* Add API authentication
* Add logging and monitoring
* Integrate AI/LLM background processing


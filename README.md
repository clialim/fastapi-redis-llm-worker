# Async LLM Inference Backend with FastAPI, Redis, and Docker

A containerized backend system demonstrating an **asynchronous LLM inference architecture** using **FastAPI**, **Redis**, and a **Llama-based worker service**.

This project separates HTTP request handling from AI inference workloads by using a **Redis job queue and pub/sub messaging pattern**.

---

# Overview

In many AI services, **LLM inference can take several seconds**.
Running inference directly inside the API server would block requests and reduce scalability.

This project demonstrates a **decoupled architecture** where:

* the **API service** handles HTTP requests
* **Redis** manages job queues and result messaging
* a **worker service** performs LLM inference

This design is commonly used in production AI systems.

---

# Tech Stack

* FastAPI
* Redis
* MySQL
* llama-cpp-python
* Docker
* Docker Compose

LLM Model:

* Llama-3.2-1B-Instruct (GGUF format)

---

# Architecture

```
Client
   │
   ▼
FastAPI API
   │
   │ push job
   ▼
Redis Queue (inference_queue)
   │
   ▼
LLM Worker
   │
   │ publish result
   ▼
Redis Pub/Sub (result:{job_id})
   │
   ▼
FastAPI API
   │
   │ Server-Sent Events (SSE)
   ▼
Client
```

Additional service:

```
FastAPI API ──► MySQL
```

---

# Request Flow

1. Client sends a POST request to `/chats`
2. API generates a unique `job_id`
3. API subscribes to Redis channel `result:{job_id}`
4. API pushes the job to Redis queue `inference_queue`
5. Worker consumes the job using `BRPOP`
6. Worker runs LLM inference
7. Worker publishes the result to `result:{job_id}`
8. API receives the result and returns it to the client

---

# Project Structure

```
.
├── api
│   ├── Dockerfile
│   ├── main.py
│   ├── database.py
│   └── requirements.txt
│
├── worker
│   ├── models
│   │   └── Llama-3.2-1B-Instruct-Q4_K_M.gguf
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Services

## API (FastAPI)

Handles HTTP requests and communicates with Redis and MySQL.

Responsibilities:

* receive client requests
* create inference jobs
* push jobs to Redis queue
* subscribe to Redis pub/sub channels
* return LLM responses to clients

API server runs on:

```
http://localhost
```

Swagger documentation:

```
http://localhost/docs
```

(Docker maps port `80 → 8000`)

---

## Worker (LLM Inference)

Background service responsible for running LLM inference.

Responsibilities:

* listen to Redis queue
* run LLM inference
* publish results back to API

Worker processes jobs continuously.

---

## Redis

Redis acts as both:

1. **Job Queue**

```
inference_queue
```

API pushes jobs using:

```
LPUSH inference_queue
```

Worker consumes jobs using:

```
BRPOP inference_queue
```

2. **Pub/Sub Messaging**

Result channel format:

```
result:{job_id}
```

Worker publishes results and API subscribes to the same channel.

---

## MySQL

MySQL is used for persistent data storage.

Configuration:

```
MYSQL_DATABASE=oz
```

Port mapping:

```
localhost:33065
```

Data is persisted using Docker volume:

```
db_data
```

---

# API Endpoint

## POST /chats

Send a question to the LLM worker.

Request:

```json
{
  "question": "What is Docker?"
}
```

Response:

```
Response: text/event-stream (streaming tokens)
```

---

# Worker Implementation

The worker continuously processes inference jobs.

```
channel = f"result:{job['id']}"

stream = create_response(question=job["question"])

for chunk in stream:
    token = chunk["choices"][0]["delta"].get("content")

    if token:
        redis_client.publish(channel, token)

redis_client.publish(channel, "[DONE]")
```

Key characteristics:

* blocking queue consumption using `BRPOP`
* sequential job processing
* result delivery through Redis pub/sub

---

# LLM Model

The worker runs a local Llama model using **llama-cpp-python**.

Place the model file in:
```
worker/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf
```

The model is loaded **once during worker startup** to avoid repeated initialization overhead.

---

# Prompt Design

The worker uses a system prompt to control response behavior.

```
SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)
```

This ensures language consistency in multilingual inputs.

---

# Running the Project

## 1 Clone the repository

```
git clone https://github.com/clialim/fastapi-redis-llm-worker.git
cd fastapi-redis-llm-worker
```

---

## 2 Place the model file

Download the GGUF model and place it in:

```
worker/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf
```

---

## 3 Build and start containers

```
docker compose up --build
```

Containers started:

```
api
worker
redis
db
```

---

## 4 Open the API

Swagger UI:

```
http://localhost/docs
```

---

# Container Network

All services communicate through a Docker bridge network.

```
backend
```

Connections:

```
api → redis
api → db
worker → redis
```

---

# Docker Volumes

MySQL data is persisted in a Docker volume.

```
db_data
```

This prevents data loss when containers restart.

---

# Possible Improvements

Potential improvements for production environments:

* job timeout handling
* retry mechanism for failed jobs
* request rate limiting
* logging and monitoring
* distributed worker scaling
* queue management using Redis Streams or Celery
* request cancellation for streaming clients


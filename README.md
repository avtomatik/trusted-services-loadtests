# trusted-services-loadtests

Async Locust-based load testing suite for the Trusted Services Platform (TSP).

Features:
- Async load tests using Locust `User` with `async def` tasks
- Postgres operations via `asyncpg`
- RabbitMQ publish operations via `aio-pika`
- Redis interactions via `redis` (async client)
- Docker Compose stack for local testing (Locust master, workers, Postgres, RabbitMQ, Redis)

---

## Quickstart (local, Docker)

### 1. Create environment file

```bash
cp .env.example .env
````

### 2. Start the full local stack

This launches:

* Locust master
* Locust worker(s)
* Postgres
* RabbitMQ
* Redis

```bash
docker compose up --build
```

### 3. Open Locust UI

[http://localhost:8089](http://localhost:8089)

Configure users + spawn rate and start the test.

---

## Running Locally (without Docker)

This project uses **uv** for dependency management.

### 1. Create venv & install dependencies

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 2. Run Locust

```bash
uv run locust -f locustfile.py
```

---

## Headless Run Example

Useful for CI or automated load tests:

```bash
uv run locust -f locustfile.py \
  --headless \
  -u 500 \
  -r 50 \
  --run-time 10m \
  --csv=results
```

---

## Distributed Mode

Locust supports distributed load generation using master + multiple workers.

* Start **master** first.
* Start one or more **workers** and point them at master.
* The included `docker-compose.yml` demonstrates this setup.

```bash
docker compose up --build
```

To scale workers:

```bash
docker compose up --scale worker=5
```

---

## Project Requirements

* Python **3.12+**
* `uv` (recommended for development)
* Docker (optional, for local infrastructure)

---

## Safety Notice

⚠️ **DO NOT** run load tests against production environments without explicit approval.

* Use sandbox / staging targets
* Use non-production databases, queues, and credentials
* Monitor resource usage to avoid accidental outages

---

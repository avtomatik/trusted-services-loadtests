# trusted-services-loadtests

Async Locust-based load testing suite for the Trusted Services Platform (TSP).

Features:
- Async tasks using Locust `User` with `async def` tasks
- Postgres (asyncpg) read/write operations
- RabbitMQ (aio-pika) publish operations
- Redis (aioredis) set/get operations
- Docker Compose stack for local testing (Locust master, workers, Postgres, RabbitMQ, Redis)

## Quickstart (local, docker)

1. Copy env file:

```bash
cp .env.example .env
````

2. Start local stack (will run Locust master + DB + RabbitMQ + Redis):

```bash
docker compose up --build
```

3. Open Locust UI: [http://localhost:8089](http://localhost:8089)

Start a test by setting number of users and spawn rate.

## Headless run (locust master)

To run headless (example):

```bash
# inside container or local virtualenv where requirements are installed
locust -f locustfile.py --headless -u 500 -r 50 --run-time 10m --csv=results
```

## Run distributed (workers)

Start master first then workers (docker-compose already includes a sample worker service). Adjust worker count for scale.

## Requirements

Python 3.12+ recommended

See `requirements.txt`.

## Safety

* **DO NOT** point this at production systems without approval.
* Use test DB/queues and sandbox environments.

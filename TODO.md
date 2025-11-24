# TODO: Redesign Load Testing Module for Trusted Services Platform

## Objective

Develop a **Locust.io-based load testing module** to evaluate the performance and stability of the **Trusted Services Platform**, focusing on:

* Database interactions
* RabbitMQ message queues
* Redis cache operations

---

## Key Components

### 1. Locust Integration

* Use **Locust.io** as the core framework for defining and executing load tests.
* Implement **custom user classes** analogous to `HttpUser`:

  * `PostgresClient` – for database interactions
  * `RabbitMQUser` – for message queue interactions
  * `RedisUser` – for cache operations
* Extend Locust’s behavior model to support **load testing chains**:

  * Define sequences of dependent operations that simulate realistic workflows (e.g., write to DB → publish to RabbitMQ → cache result in Redis).
  * Support conditional logic and branching within chains.
  * Allow combined metrics collection across multi-step test flows.

---

### 2. Functional Targets

#### Database

* Implement a connector to interact directly with the database.
* Simulate realistic query loads and transaction scenarios.
* Support regression testing to compare performance over time.

#### RabbitMQ

* Develop functionality to:

  * Read messages from a queue without permanently consuming them.
  * Requeue messages after inspection to preserve queue state.
* Handle edge cases such as empty queues or malformed messages.
* Allow inspection of queue contents during test runs.

#### Redis

* Implement a connector for Redis.
* Support read-only operations for inspecting cache or queue contents.
* Ensure non-destructive access (view data without clearing or altering it).

---

## Load Testing Chains

The module should provide a way to **compose complex, multi-service load testing scenarios**.
Example workflow:

1. A simulated user writes data to the database.
2. The system publishes an event to RabbitMQ.
3. A background consumer processes the event and writes to Redis.
4. The test validates the consistency and latency of all steps.

Chains can be configured declaratively (e.g., via YAML/JSON scenarios) or programmatically through custom Locust task definitions.
This enables modeling of realistic end-to-end transaction flows across distributed system components.

---

## Testing and Analysis

* Capture and log performance metrics such as latency, throughput, and error rates.
* Produce structured output logs and reports (e.g., `results_*.csv`).
* Enable regression testing to detect performance regressions compared to previous runs.

---

## Implementation Notes

* Use browser DevTools (F12) to analyze real backend requests and model realistic load scenarios.
* Consider LLM-assisted generation or optimization of test cases based on observed traffic patterns or API definitions.
* Prepare an extensible connector interface to integrate Locust with non-HTTP services (DB, MQ, Cache).

---

## Current Status

* Base Locust setup complete and functioning (`wip/loadtest-async` branch).
* Load test results successfully logged to CSV files.
* Initial `docker-compose.yml` drafted (not yet tested).
* Next step: implement custom Locust user classes for database, RabbitMQ, and Redis, and define prototype load testing chains.

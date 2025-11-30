import time

from locust import User, constant, task

from clients.db import PostgresClient
from clients.mq import RabbitMQClient
from clients.redis import RedisClient
from core.config import settings
from utils.timing import SECONDS_TO_MILLISECONDS


class BackendUser(User):
    abstract = True
    wait_time = constant(1)

    def on_start(self):
        self.db = PostgresClient(settings.db_dsn)
        self.mq = RabbitMQClient(settings.mq_url)
        self.redis = RedisClient(settings.redis_url)

        self.db.connect()
        self.mq.connect()
        self.redis.connect()

    def on_stop(self):
        self.db.close()
        self.mq.close()
        self.redis.close()


class TSPLoadUser(BackendUser):
    @task(3)
    def query_db(self):
        with self.environment.events.request.request(
            request_type="postgres", name="select_count"
        ) as req:
            val = self.db.fetch_count("value")
            req.response_length = len(str(val))

    @task(2)
    def insert_db(self):
        with self.environment.events.request.request(
            request_type="postgres", name="insert"
        ) as req:
            self.db.insert_row("Some log message")
            req.response_length = 0

    @task(4)
    def publish_message(self):
        payload = {"ts": time.time(), "payload": "sync_test"}

        with self.environment.events.request.request(
            request_type="rabbit", name="publish"
        ) as req:
            self.mq.publish(payload)
            req.response_length = len(str(payload))

    @task(3)
    def redis_ops(self):
        key = f"test:{int(time.time() * SECONDS_TO_MILLISECONDS)}"

        with self.environment.events.request.request(
            request_type="redis", name="set_get"
        ) as req:

            self.redis.set_key(key, "value", expire=120)
            val = self.redis.get_key(key)
            req.response_length = len(val or "")

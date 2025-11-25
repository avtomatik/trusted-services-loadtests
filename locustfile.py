import time

from locust import User, constant, events, task

from clients.db import PostgresClient
from clients.mq import RabbitMQClient
from clients.redis import RedisClient
from core.config import settings
from utils.timing import SECONDS_TO_MILLISECONDS, get_run_time_in_ms


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
        start = time.perf_counter()
        try:
            self.db.fetch_count('value')
            response_time = get_run_time_in_ms(start)
            events.request_success.fire(
                request_type='postgres',
                name='select_count',
                response_time=response_time,
                response_length=0
            )
        except Exception as e:
            response_time = get_run_time_in_ms(start)
            events.request_failure.fire(
                request_type='postgres',
                name='select_count',
                response_time=response_time,
                exception=e
            )

    @task(2)
    def insert_db(self):
        start = time.perf_counter()
        try:
            self.db.insert_row('Some log message')
            response_time = get_run_time_in_ms(start)
            events.request_success.fire(
                request_type='postgres',
                name='insert',
                response_time=response_time,
                response_length=0
            )
        except Exception as e:
            response_time = get_run_time_in_ms(start)
            events.request_failure.fire(
                request_type='postgres',
                name='insert',
                response_time=response_time,
                exception=e
            )

    @task(4)
    def publish_message(self):
        start = time.perf_counter()
        try:
            payload = {'ts': time.time(), 'payload': 'sync_test'}
            self.mq.publish(payload)
            response_time = get_run_time_in_ms(start)
            events.request_success.fire(
                request_type='rabbit',
                name='publish',
                response_time=response_time,
                response_length=len(str(payload))
            )
        except Exception as e:
            response_time = get_run_time_in_ms(start)
            events.request_failure.fire(
                request_type='rabbit',
                name='publish',
                response_time=response_time,
                exception=e
            )

    @task(3)
    def redis_ops(self):
        start = time.perf_counter()
        try:
            key = f'test:{int(time.time() * SECONDS_TO_MILLISECONDS)}'
            self.redis.set_key(key, 'value', expire=120)
            val = self.redis.get_key(key)
            response_time = get_run_time_in_ms(start)
            events.request_success.fire(
                request_type='redis',
                name='set_get',
                response_time=response_time,
                response_length=len(val or '')
            )
        except Exception as e:
            response_time = get_run_time_in_ms(start)
            events.request_failure.fire(
                request_type='redis',
                name='set_get',
                response_time=response_time,
                exception=e
            )

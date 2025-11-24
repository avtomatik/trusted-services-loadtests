import asyncio
import os
import time

from dotenv import load_dotenv
from locust import User, between, events, task

from clients.db import AsyncDBClient
from clients.mq import AsyncMQClient
from clients.redis import AsyncRedisClient
from core.config import settings

load_dotenv()


class AsyncBackendUser(User):
    abstract = True
    wait_time = between(0.5, 2)

    async def on_start(self):
        self.db = PostgresClient(settings.db_dsn)
        self.mq = RabbitMQClient(settings.mq_url)
        self.redis = RedisClient(settings.redis_url)

        self.db.connect()
        self.mq.connect()
        self.redis.connect()

        await asyncio.gather(
            self.db.connect(),
            self.mq.connect(),
            self.redis.connect()
        )

    async def on_stop(self):
        await asyncio.gather(
            self.db.close(),
            self.mq.close(),
            self.redis.close()
        )


class TSPLoadUser(AsyncBackendUser):
    @task(3)
    async def query_db(self):
        start = time.perf_counter()
        try:
            await self.db.fetch_count('value')
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
    async def insert_db(self):
        start = time.perf_counter()
        try:
            await self.db.insert_row('a', 'b')
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
    async def publish_message(self):
        start = time.perf_counter()
        try:
            payload = {'ts': time.time(), 'payload': 'async_test'}
            await self.mq.publish(payload)
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
    async def redis_ops(self):
        start = time.perf_counter()
        try:
            key = f'test:{int(time.time() * 1000)}'
            await self.redis.set_key(key, 'value', expire=120)
            val = await self.redis.get_key(key)
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

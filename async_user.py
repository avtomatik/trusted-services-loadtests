from http import HTTPStatus

import psycopg
from locust import FastHttpUser, constant, task

from core.config import settings
from utils.sql import load_sql

SQL_SELECT_USERS = load_sql('select_users.sql')
SQL_INSERT_LOG = load_sql('insert_log.sql')
SQL_UPDATE_LAST_ACCESS = load_sql('update_last_access.sql')


class AsyncUser(FastHttpUser):
    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_conn = None

    async def on_start(self):
        self.db_conn = await psycopg.AsyncConnection.connect(settings.db_dsn)

    async def on_stop(self):
        if self.db_conn:
            await self.db_conn.close()

    @task
    async def get_recent_users(self):
        async with self.db_conn.cursor() as cursor:
            await cursor.execute(SQL_SELECT_USERS)
            results = await cursor.fetchall()
            # Some processing made here
            assert len(results) > 0, "Нет данных"

    @task
    async def insert_log(self):
        async with self.db_conn.cursor() as cursor:
            message = "Test log"
            await cursor.execute(SQL_INSERT_LOG, (message,))
            await self.db_conn.commit()

    @task
    async def http_get_and_update_last_access(self):
        response = await self.client.get("/api/users")
        if response.status_code == HTTPStatus.OK:
            async with self.db_conn.cursor() as cursor:
                user_id = 1
                await cursor.execute(SQL_UPDATE_LAST_ACCESS, (user_id,))
                await self.db_conn.commit()

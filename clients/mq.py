import json

from aio_pika import (Channel, DeliveryMode, Message, RobustConnection,
                      connect_robust)


class AsyncMQClient:
    def __init__(self, url: str, queue_name: str = 'test_queue'):
        self.url = url
        self.queue_name = queue_name
        self.connection: RobustConnection | None = None
        self.channel: Channel | None = None

    async def connect(self):
        if self.connection is None:
            self.connection = await connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue_name, durable=True)

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None

    async def publish(self, payload: dict):
        body = json.dumps(payload).encode()
        message = Message(body, delivery_mode=DeliveryMode.PERSISTENT)
        await self.channel.default_exchange.publish(
            message,
            routing_key=self.queue_name
        )

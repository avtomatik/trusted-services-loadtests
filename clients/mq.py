import json

import pika


class RabbitMQClient:
    def __init__(self, url: str, queue_name: str = 'test_queue'):
        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        if self.connection is None:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.url)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.channel = None

    def publish(self, payload: dict):
        body = json.dumps(payload).encode()
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent
        )

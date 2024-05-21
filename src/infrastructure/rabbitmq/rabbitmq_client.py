import pika
from app.core.config import settings


class RabbitMQClient:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT
            )
        )
        self.channel = connection.channel()

    def publish(self, queue: str, message: str):
        self.channel.basic_publish(exchange="", routing_key=queue, body=message)

    def consume(self, queue: str, callback):
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

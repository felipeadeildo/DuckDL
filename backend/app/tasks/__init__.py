import dramatiq
from app.config import settings
from dramatiq.middleware import AsyncIO
from dramatiq.brokers.rabbitmq import RabbitmqBroker

rabbitmq_broker = RabbitmqBroker(url=settings.rabbitmq_url)

rabbitmq_broker.add_middleware(AsyncIO())

dramatiq.set_broker(rabbitmq_broker)

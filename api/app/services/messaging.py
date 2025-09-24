import asyncio
from aio_pika import connect_robust, Message, ExchangeType
from app.core.config import get_settings

class RabbitPublisher:
    def __init__(self):
        self._conn = None
        self._channel = None

    async def connect(self):
        settings = get_settings()
        self._conn = await connect_robust(settings.amqp_url)
        self._channel = await self._conn.channel()
        return self

    async def publish_json(self, routing_key: str, payload: dict, exchange: str = "events"):
        assert self._channel is not None
        ex = await self._channel.declare_exchange(exchange, ExchangeType.TOPIC, durable=True)
        body = Message(body=__import__('json').dumps(payload).encode('utf-8'))
        await ex.publish(body, routing_key=routing_key)

    async def close(self):
        if self._conn:
            await self._conn.close()

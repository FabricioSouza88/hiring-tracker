import asyncio
from aio_pika import connect_robust, Message, DeliveryMode, ExchangeType, IncomingMessage
from contextlib import asynccontextmanager
from appdirs import user_cache_dir  # not strictly necessary; could be used for idempotency file cache
from .settings import get_settings
from .logging import get_logger

logger = get_logger()

class MQ:
    def __init__(self):
        self.conn = None
        self.channel = None

    async def connect(self):
        s = get_settings()
        self.conn = await connect_robust(s.amqp_url)
        self.channel = await self.conn.channel()
        await self.channel.set_qos(prefetch_count=s.prefetch)
        logger.info("mq_connected", url=s.amqp_url)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def declare_topology(self):
        assert self.channel is not None
        events = await self.channel.declare_exchange("events", ExchangeType.TOPIC, durable=True)
        # Declare queues for each agent
        triage_q = await self.channel.declare_queue("agent.triage", durable=True)
        await triage_q.bind(events, routing_key="agent.triage.requested")

        code_q = await self.channel.declare_queue("agent.code", durable=True)
        await code_q.bind(events, routing_key="agent.code_evaluator.requested")

        judge_q = await self.channel.declare_queue("agent.judge", durable=True)
        await judge_q.bind(events, routing_key="agent.judge.requested")

        return {"events": events, "triage_q": triage_q, "code_q": code_q, "judge_q": judge_q}

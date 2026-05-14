from typing import Dict, Any
import aio_pika
import json
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

class EventPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def initialize(self, rabbitmq_url: str = "amqp://guest:guest@localhost/"):
        self.connection = await aio_pika.connect_robust(rabbitmq_url)
        self.channel = await self.connection.channel()

        # Declare exchange
        self.exchange = await self.channel.declare_exchange(
            "executive-agent-events", aio_pika.ExchangeType.TOPIC
        )

    async def publish(self, event_type: str, payload: Dict[str, Any], routing_key: str = None):
        """Publish an event"""
        if routing_key is None:
            routing_key = event_type.lower()

        event = {
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "orchestrator"
        }

        message = aio_pika.Message(
            body=json.dumps(event).encode(),
            content_type="application/json"
        )

        if getattr(self, "exchange", None) is None:
            logger.warning("Event publisher not initialized, logging event locally", event_type=event_type, routing_key=routing_key)
            logger.info("Event payload", payload=payload)
            return

        await self.exchange.publish(message, routing_key=routing_key)
        logger.info("Event published", event_type=event_type, routing_key=routing_key)

    async def close(self):
        if self.connection:
            await self.connection.close()
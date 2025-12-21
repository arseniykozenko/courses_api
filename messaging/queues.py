from messaging.rabbitmq import channel

# Основные очереди
REQUEST_QUEUE = "api.requests"
RESPONSE_QUEUE = "api.responses"
DLQ_QUEUE = "api.dlq"

channel.queue_declare(
    queue=REQUEST_QUEUE,
    durable=True,
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": DLQ_QUEUE
    }
)

channel.queue_declare(
    queue=RESPONSE_QUEUE,
    durable=True
)

channel.queue_declare(
    queue=DLQ_QUEUE,
    durable=True
)
REQUEST_QUEUE = "api.requests"
DLQ_QUEUE = "api.dlq"

def declare_queues(channel):
    channel.queue_declare(
        queue=REQUEST_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": DLQ_QUEUE,
        }
    )

    channel.queue_declare(
        queue=DLQ_QUEUE,
        durable=True
    )
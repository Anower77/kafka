import json
from confluent_kafka import Producer


KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
}

TOPIC = "orders"


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
        return

    print(
        f"Message delivered | "
        f"topic={msg.topic()} | "
        f"partition={msg.partition()} | "
        f"offset={msg.offset()}"
    )


producer = Producer(KAFKA_CONFIG)


for order_id in range(1, 1000000001):

    order = {
        "order_id": order_id,
        "customer": f"Customer-{order_id}",
        "amount": order_id * 100,
    }

    while True:
        try:
            producer.produce(
                TOPIC,
                key=str(order_id),
                value=json.dumps(order),
                callback=delivery_report,
            )
            break

        except BufferError:
            # Wait for previously queued messages
            # to be delivered before adding more.
            producer.poll(1)


    # Process delivery callbacks and events
    producer.poll(0)


# Wait until all queued messages are delivered
producer.flush()

print("All messages delivered.")



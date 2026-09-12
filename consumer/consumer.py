import json
from confluent_kafka import Consumer


KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-consumer-group",
    "auto.offset.reset": "earliest",
}

TOPIC = "orders"


consumer = Consumer(KAFKA_CONFIG)

consumer.subscribe([TOPIC])

print("Consumer started. Waiting for messages...")


try:
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        order = json.loads(message.value().decode("utf-8"))

        print("\nReceived order:")
        print(f"Order ID: {order['order_id']}")
        print(f"Customer: {order['customer']}")
        print(f"Amount: {order['amount']}")

        print(
            f"Topic: {message.topic()} | "
            f"Partition: {message.partition()} | "
            f"Offset: {message.offset()}"
        )

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
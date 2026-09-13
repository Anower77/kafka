import json
import time

from confluent_kafka import Producer


KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",

    # Durability
    "acks": "all",

    # Throughput
    "batch.size": 65536,
    "linger.ms": 10,
    "compression.type": "lz4",

    # Producer buffer
    "queue.buffering.max.messages": 100000,

    # Retry transient failures
    "retries": 10,
}

TOPIC = "orders"


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
        return

    # Don't print every message when doing
    # throughput benchmarks.
    pass


producer = Producer(KAFKA_CONFIG)

start_time = time.perf_counter()

message_count = 100_000

for order_id in range(1, message_count + 1):

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
            # Local producer queue is full.
            # Wait for Kafka to deliver messages.
            producer.poll(1)

    # Process delivery events.
    producer.poll(0)


# Wait for all outstanding messages.
producer.flush()

end_time = time.perf_counter()

elapsed = end_time - start_time

print()
print("========== BENCHMARK ==========")
print(f"Messages : {message_count:,}")
print(f"Time     : {elapsed:.2f} seconds")
print(f"Rate     : {message_count / elapsed:,.0f} messages/sec")
print("================================")
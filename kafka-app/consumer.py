import sys
import json

from kafka import KafkaConsumer

from client import KAFKA_BROKER


def init():
    if len(sys.argv) < 2:
        print("Usage: python consumer.py <group_id>")
        sys.exit(1)

    group = sys.argv[1]

    consumer = KafkaConsumer(
        "rider-updates",
        bootstrap_servers=KAFKA_BROKER,
        group_id=group,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )

    print(f"Consumer started with group: {group}")

    try:
        for message in consumer:
            print(
                f"{group}: "
                f"[{message.topic}]: "
                f"PART:{message.partition}: "
                f"{message.value}"
            )

    except KeyboardInterrupt:
        print("\nStopping Consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    init()
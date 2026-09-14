from kafka import KafkaProducer
import json

from client import KAFKA_BROKER


def init():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda key: key.encode("utf-8"),
    )

    print("Connecting Producer...")
    print("Producer Connected Successfully")

    try:
        while True:
            line = input("> ")

            if not line:
                continue

            parts = line.split()

            if len(parts) != 2:
                print("Usage: <rider_name> <location>")
                continue

            rider_name, location = parts

            partition = (
                0
                if location.lower() == "north"
                else 1
            )

            message = {
                "name": rider_name,
                "location": location,
            }

            producer.send(
                "rider-updates",
                key="location-update",
                value=message,
                partition=partition,
            )

            producer.flush()

    except KeyboardInterrupt:
        print("\nStopping Producer...")

    finally:
        producer.close()


if __name__ == "__main__":
    init()
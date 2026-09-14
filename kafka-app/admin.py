from kafka.admin import KafkaAdminClient, NewTopic
from client import KAFKA_BROKER


def init():
    admin = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id="my-app",
    )

    print("Admin connecting...")
    print("Admin Connection Success...")

    topic_name = "rider-updates"

    print(f"Creating Topic [{topic_name}]")

    topic = NewTopic(
        name=topic_name,
        num_partitions=2,
        replication_factor=1,
    )

    try:
        admin.create_topics(
            new_topics=[topic],
            validate_only=False,
        )

        print(f"Topic Created Success [{topic_name}]")

    except Exception as error:
        print(f"Topic creation failed: {error}")

    finally:
        print("Disconnecting Admin...")
        admin.close()


if __name__ == "__main__":
    init()
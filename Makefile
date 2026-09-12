(Get-Content .\Makefile) -replace '^ {8}', "`t" | Set-Content .\Makefile

# ============================================================
# Kafka Practice - Makefile
# ============================================================
#
# This Makefile provides shortcuts for common development
# and Kafka management commands.
#
# Usage:
#   make <command>
#
# Example:
#   make up
#   make topic
#   make producer
#   make consumer
# ============================================================


# ------------------------------------------------------------
# Docker Commands
# ------------------------------------------------------------

# Start Kafka container in detached mode
up:
	docker compose up -d


# Stop and remove Kafka containers
down:
	docker compose down


# Restart Kafka container
restart:
	docker compose restart


# Show running Docker containers
ps:
	docker compose ps


# Show Kafka container logs
logs:
	docker logs kafka -f


# Follow Kafka logs in real time
logs-follow:
	docker logs -f kafka


# ------------------------------------------------------------
# Kafka Topic Commands
# ------------------------------------------------------------

# Create the "orders" topic with 3 partitions
topic:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-topics.sh \
		--create \
		--topic orders \
		--bootstrap-server localhost:9092 \
		--partitions 3 \
		--replication-factor 1


# List all Kafka topics
topics:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-topics.sh \
		--list \
		--bootstrap-server localhost:9092


# Show detailed information about the orders topic
topic-info:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-topics.sh \
		--describe \
		--topic orders \
		--bootstrap-server localhost:9092


# Delete the orders topic
topic-delete:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-topics.sh \
		--delete \
		--topic orders \
		--bootstrap-server localhost:9092


# ------------------------------------------------------------
# Python Commands
# ------------------------------------------------------------

# Create a Python virtual environment
venv:
	python -m venv .venv


# Install Python dependencies
install:
	pip install confluent-kafka


# Run the Kafka producer
producer:
	python producer/producer.py


# Run the Kafka consumer
consumer:
	python consumer/consumer.py


# ------------------------------------------------------------
# Kafka Debugging Commands
# ------------------------------------------------------------

# Start a Kafka console producer
console-producer:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-console-producer.sh \
		--topic orders \
		--bootstrap-server localhost:9092


# Start a Kafka console consumer
console-consumer:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-console-consumer.sh \
		--topic orders \
		--bootstrap-server localhost:9092 \
		--from-beginning


# Show consumer group information
consumer-groups:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-consumer-groups.sh \
		--bootstrap-server localhost:9092 \
		--list


# Show details about our order consumer group
consumer-group-info:
	docker exec -it kafka \
		/opt/kafka/bin/kafka-consumer-groups.sh \
		--bootstrap-server localhost:9092 \
		--describe \
		--group order-consumer-group


# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------

# Stop Kafka and remove containers and volumes
# WARNING: This removes Kafka's persisted data.
clean:
	docker compose down -v

cm ?= Update code

git:
	git add .
	git status
	git commit -m "$(cm)"
	git log -1 --graph --oneline
	git push origin main


# ------------------------------------------------------------
# Help
# ------------------------------------------------------------

# Display available Make commands
help:
	@echo "Kafka Practice Commands:"
	@echo ""
	@echo "Docker:"
	@echo "  make up                  Start Kafka"
	@echo "  make down                Stop Kafka"
	@echo "  make restart             Restart Kafka"
	@echo "  make ps                  Show containers"
	@echo "  make logs                Show Kafka logs"
	@echo "  make logs-follow         Follow Kafka logs"
	@echo ""
	@echo "Topics:"
	@echo "  make topic               Create orders topic"
	@echo "  make topics              List topics"
	@echo "  make topic-info          Describe orders topic"
	@echo "  make topic-delete        Delete orders topic"
	@echo ""
	@echo "Python:"
	@echo "  make venv                Create virtual environment"
	@echo "  make install             Install dependencies"
	@echo "  make producer            Run Python producer"
	@echo "  make consumer            Run Python consumer"
	@echo ""
	@echo "Debugging:"
	@echo "  make console-producer    Start Kafka CLI producer"
	@echo "  make console-consumer    Start Kafka CLI consumer"
	@echo "  make consumer-groups     List consumer groups"
	@echo "  make consumer-group-info Show consumer group details"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean               Remove containers and volumes"


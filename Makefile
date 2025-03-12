VERSION=latest

deps:
	pip install -r requirements.txt

build:
	docker build \
	--rm=true \
	--platform=linux/amd64 \
	-t docker.io/bborbe/sample-kafka-consumer:$(VERSION) \
	-f Dockerfile .

run:
	docker kill sample-kafka-consumer || true
	docker run \
	--rm \
	--name sample-kafka-consumer \
	--platform=linux/amd64 \
	--net=host \
	-e LISTEN=0.0.0.0:9090 \
	-e KAFKA_BROKER=127.0.0.1:9092 \
	-e KAFKA_GROUP=test-group \
	-e KAFKA_TOPIC=test-topic \
	-p 9090:9090 \
	docker.io/bborbe/sample-kafka-consumer:$(VERSION)

format:
	docker run \
	-ti \
	-v ./data:/tmp/kraft-combined-logs \
	-e CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk \
	apache/kafka:latest \
	sh -c '/opt/kafka/bin/kafka-storage.sh format -t MkU3OEVBNTcwNTJENDM2Qk -c /opt/kafka/config/kraft/server.properties'

kafka:
	docker compose up

createtopic:
	docker exec -ti \
	broker \
	/opt/kafka/bin/kafka-topics.sh --create --topic test-topic --bootstrap-server broker:9092

produce:
	docker exec -ti \
	broker \
	/opt/kafka/bin/kafka-console-producer.sh  --topic test-topic --bootstrap-server broker:9092

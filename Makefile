VERSION=latest

deps:
	pip install -r requirements.txt

run:
	python main.py \
	--listen='0.0.0.0:9090' \
	--kafka-broker='127.0.0.1:9092' \
	--kafka-group='test-group' \
	--kafka-topic=test-topic

download:
	mkdir -p kafka
	curl -Ls "https://dlcdn.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz" | tar -xz --directory kafka --strip-components=1 --no-same-owner
	echo "auto.create.topics.enable=true" >> kafka/config/kraft/reconfig-server.properties

format:
	kafka/bin/kafka-storage.sh format --standalone -t "$$(kafka/bin/kafka-storage.sh random-uuid)" -c kafka/config/kraft/reconfig-server.properties

kafka:
	kafka/bin/kafka-server-start.sh kafka/config/kraft/reconfig-server.properties

.PHONY: kafka

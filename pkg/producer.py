import logging

import confluent_kafka


class Producer:
    def __init__(
            self,
            kafka_broker: str,
    ) -> None:
        self.producer = confluent_kafka.Producer({
            'bootstrap.servers': kafka_broker,
            'client.id': 'python-producer'
        })

    def send_message(self, kafka_topic: str, key: str | bytes, value: str | bytes) -> None:
        self.producer.produce(
            topic=kafka_topic,
            key=key,
            value=value,
        )
        logging.info(f'sent message to {kafka_topic} with key {str(key)} completed')

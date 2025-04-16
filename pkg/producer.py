import logging

import confluent_kafka


class Producer:
    def __init__(
            self,
            kafka_broker: str,
            kafka_tls: bool,
    ) -> None:
        config = {
            'bootstrap.servers': kafka_broker,
            'client.id': 'python-producer',
        }
        if kafka_tls:
            config.update({
                'security.protocol': 'SSL',
                'enable.ssl.certificate.verification': False,
                'ssl.ca.location': './ca.crt',
                'ssl.certificate.location': './user.crt',
                'ssl.key.location': './user.key',
            })

        self.producer = confluent_kafka.Producer(config)

    def send_message(self, kafka_topic: str, key: str | bytes, value: str | bytes) -> None:
        self.producer.produce(
            topic=kafka_topic,
            key=key,
            value=value,
        )
        logging.info(f'sent message to {kafka_topic} with key {str(key)} completed')

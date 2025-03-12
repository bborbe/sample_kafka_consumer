import logging
import traceback

import confluent_kafka


class MessageHandler:
    def __init__(self):
        pass

    def handle_message(self, message: confluent_kafka.Message):
        logging.info("handle message %d started", message.offset)
        logging.info("Got Record - {}".format(message))
        logging.info("handle message %d completed", message.offset)


class MessageHandlerFunc(MessageHandler):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def handle_message(self, message: confluent_kafka.Message):
        self.fn(message)


class Consumer:

    def __init__(
            self,
            message_handler: MessageHandler,
            kafka_broker: str,
            kafka_group: str,
            kafka_topic: str,
    ):
        self.running = True
        self.timeout = 30.0
        self.num_messages = 1
        self.message_handler = message_handler
        self.consumer = confluent_kafka.Consumer({
            'bootstrap.servers': kafka_broker,
            'group.id': kafka_group,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([kafka_topic])
        logging.info(f"Consumer subscribed to topic {kafka_topic}")

    def consume(self):
        logging.info("consume started")
        try:
            while self.running:
                logging.info("wait for messages")
                messages = self.consumer.consume(num_messages=self.num_messages, timeout=self.timeout)
                for msg in messages:
                    if msg is None:
                        continue
                    if msg.error():
                        logging.error(f"Consumer error: {msg.error()}")
                        continue
                    logging.info("handle mesage started")
                    self.message_handler.handle_message(msg)
                    logging.info("handle mesage completed")
        except Exception as e:
            logging.warning(f'consume failed: {e}')
            traceback.print_exc()
            raise e
        finally:
            self.shutdown()

    def shutdown(self):
        self.running = False
        self.consumer.unsubscribe()
        self.consumer.close()
        logging.info("consumer closed")

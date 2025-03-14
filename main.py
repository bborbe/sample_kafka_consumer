#!/usr/bin/env python3
import getopt
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import logging
import signal
import sentry_sdk
from confluent_kafka import Message
from sentry_sdk import capture_exception
from pkg import runner, http
from pkg.consumer import Consumer
from pkg.message_handler import MessageHandlerFunc
from pkg.producer import Producer


def main(argv):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    opts, args = getopt.getopt(argv, 'h', [
        'listen=',
        'sentry-dsn=',
        'debug=',
        'kafka-group=',
        'kafka-broker=',
        'kafka-topic=',
    ])
    listen: str = os.getenv('LISTEN')
    sentry_dsn: str = os.getenv('SENTRY_DSN')
    kafka_broker: str = os.getenv('KAFKA_BROKER')
    kafka_group: str = os.getenv("KAFKA_GROUP")
    kafka_topic: str = os.getenv("KAFKA_TOPIC")

    for opt, arg in opts:
        if opt == '-h':
            logging.info('main.py --port 8080')
            sys.exit()
        elif opt in ('-kafka-broker', '--kafka-broker'):
            kafka_broker = arg
        elif opt in ('-kafka-group', '--kafka-group'):
            kafka_group = arg
        elif opt in ('-kafka-topic', '--kafka-topic'):
            kafka_topic = arg
        elif opt in ('-listen', '--listen'):
            listen = arg
        elif opt in ('-debug', '--debug'):
            logger = logging.getLogger()
            logger.setLevel(level=logging.DEBUG)
        elif opt in ('-sentry-dsn', '--sentry-dsn'):
            sentry_dsn = arg

    logging.info(f'listen = {listen}')
    logging.info(f'sentry_dsn = {sentry_dsn}')
    logging.info(f'kafka_broker = {kafka_broker}')
    logging.info(f'kafka_group = {kafka_group}')
    logging.info(f'kafka_topic = {kafka_topic}')

    sentry_sdk.init(
        dsn=sentry_dsn,
    )

    def handle_message(message: Message):
        message_key = 'None' if message.key() is None else message.key().decode('utf-8')
        message_value = 'None' if message.value() is None else message.value().decode('utf-8')
        logging.info(f"key: {message_key} value: {message_value}")

    consumer = Consumer(
        kafka_broker=kafka_broker,
        kafka_group=kafka_group,
        kafka_topic=kafka_topic,
        message_handler=MessageHandlerFunc(handle_message)
    )

    host, port = listen.split(":", 2)
    server = http.Server(
        host=host,
        port=int(port),
        producer=Producer(
            kafka_broker=kafka_broker,
        ),
        kafka_topic=kafka_topic,
    )

    def shutdown():
        logging.info('shutdown started')

        server.shutdown()
        logging.info('server.shutdown() completed')

        consumer.shutdown()
        logging.info('consumer.shutdown() completed')

        logging.info('shutdown complete => exit(0)')
        sys.exit(0)

    def stop(signal_number, frame):
        logging.info('SIGTERM, shutting down.')
        shutdown()

    def on_error(exception: Exception):
        logging.info(f'on_error for exception {exception} started')
        capture_exception(exception)
        shutdown()
        logging.info(f'on_error for exception {exception} completed')

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            runner.Runner(
                server.run,
                on_error,
            ).run,
        )
        executor.submit(
            runner.Runner(
                consumer.consume,
                on_error,
            ).run,
        )


if __name__ == '__main__':
    main(sys.argv[1:])

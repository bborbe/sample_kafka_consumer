from http.server import HTTPServer
from socketserver import ThreadingMixIn
from prometheus_client import MetricsHandler
import logging

from pkg.producer import Producer


class Server:
    def __init__(self, host: str, port: int, producer: Producer, kafka_topic: str):
        logging.info(f'Server started http://{host}:{port}')
        handler_class = SimpleRequestHandler
        self.server = ThreadedHTTPServer(
            (host, port),
            lambda *args, **kwargs: handler_class(
                *args,
                producer=producer,
                kafka_topic=kafka_topic,
                **kwargs,
            )
        )

    def run(self):
        try:
            self.server.serve_forever()
        finally:
            self.shutdown()

    def shutdown(self):
        self.server.server_close()
        logging.info("httpServer closed")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class SimpleRequestHandler(MetricsHandler):
    def __init__(self, *args, producer: Producer, kafka_topic: str, **kwargs):
        self.producer = producer
        self.kafka_topic = kafka_topic
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/setloglevel/debug":
            logging.getLogger().setLevel(logging.DEBUG)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'set loglevel = DEBUG')
        elif self.path == "/setloglevel/info":
            logging.getLogger().setLevel(logging.INFO)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'set loglevel = INFO')
        elif self.path == "/readiness":
            logging.debug("readiness")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == "/healthz":
            logging.debug("readiness")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == "/sendmessage":
            self.producer.send_message(
                self.kafka_topic,
                '1337',
                'hello world',
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'send message completed')
            logging.debug("send message completed")
        else:
            MetricsHandler.do_GET(self)

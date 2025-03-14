from abc import abstractmethod
from typing import Callable
from confluent_kafka import Message


class MessageHandler:
    def __init__(self):
        pass

    @abstractmethod
    def handle_message(self, message: Message) -> None:
        pass


class MessageHandlerFunc(MessageHandler):
    def __init__(self, fn: Callable[[Message], None]):
        super().__init__()
        self.fn = fn

    def handle_message(self, message: Message) -> None:
        self.fn(message)

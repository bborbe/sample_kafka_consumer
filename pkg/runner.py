import logging
import traceback
from typing import Callable


class Runner:
    def __init__(self, action: Callable[[], None], on_error: Callable[[Exception], None]):
        self.action = action
        self.on_error = on_error

    def run(self):
        try:
            logging.info('run action started')
            result = self.action()
            logging.info('run action completed')
            return result
        except Exception as e:
            logging.warning(f'run failed: {e}')
            traceback.print_exc()
            logging.info('run on_error started')
            self.on_error(e)
            logging.info('run on_error completed')

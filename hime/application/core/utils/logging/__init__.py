from __future__ import annotations
import logging
import sys

class Log:
    _logging: logging.Logger = None

    def __init__(self):
        self._logging = self._initialize_log()

    def _initialize_log(self) -> logging.Logger:
        logging.basicConfig(level=logging.INFO)
        log: logging.Logger = logging.getLogger('manga-translator-logger')
        log.propagate = False

        log_format = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s - %(message)s')
        logging_handler = logging.StreamHandler(sys.stdout)
        logging_handler.setLevel(logging.NOTSET)
        logging_handler.setFormatter(log_format)

        log.addHandler(logging_handler)

        return log

    def info(self, message: str) -> None:
        self._logging.info(message)

    def error(self, message: str, stack_trace: str=None) -> None:
        self._logging.error(message)
        if stack_trace is not None: self._logging.error(stack_trace)
        
logger = Log()
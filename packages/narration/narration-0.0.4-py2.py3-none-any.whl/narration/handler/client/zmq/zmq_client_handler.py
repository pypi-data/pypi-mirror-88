import logging
import threading

import zmq

from queue import Queue

from narration.handler.client.base_client_handler import BaseClientHandler
from narration.handler.client.base_sender_thread import BaseSenderThread
from narration.handler.client.zmq.zmq_sender_thread import ZmqSenderThread


class ZMQClientHandler(BaseClientHandler):
    def __init__(self, name=None, address: str = None, level=logging.DEBUG):
        super(ZMQClientHandler, self).__init__(name=name, queue=Queue(-1), level=level)

        self._socket_type = zmq.PUSH
        self._address = address

        self._start_background_processing()

    def _create_background_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseSenderThread:
        return ZmqSenderThread(
            name=thread_name,
            sender_ready=processing_ready,
            socket_type=self._socket_type,
            address=self._address,
            queue=self._queue,
        )


# import logging
# from logging import LogRecord
#
# class ZMQClientHandler(BaseClientHandler):
#     def acquire(self):
#         self.target_handler.acquire()
#
#     def release(self):
#         self.target_handler.release()
#
#     def addFilter(self, filter):
#         self.target_handler.addFilter(filter)
#
#     def close(self):
#         self.target_handler.close()
#
#     def createLock(self) -> None:
#         self.target_handler.createLock()
#
#     def emit(self, record):
#         self.target_handler.emit(record)
#
#     def filter(self, record: LogRecord) -> bool:
#         return self.target_handler.filter(record)
#
#     def flush(self) -> None:
#         self.target_handler.flush()
#
#     def format(self, record: LogRecord) -> str:
#         return self.target_handler.format(record)
#
#     def handle(self, record: LogRecord):
#         self.target_handler.handle(record)
#
#     def handleError(self, record: LogRecord):
#         self.target_handler.handleError(record)
#
#     def setFormatter(self, fmt, level=logging.DEBUG):
#         self.target_handler.setFormatter(fmt, level=level)
#
#     def setLevel(self, level=logging.DEBUG):
#         self.target_handler.setLevel(level)

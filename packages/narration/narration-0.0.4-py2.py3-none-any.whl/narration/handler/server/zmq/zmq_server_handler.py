import logging
import threading

import zmq

from narration.handler.server.base_server_handler import HandlerType, BaseServerHandler
from narration.handler.common.base_receiver_thread import BaseReceiverThread
from narration.handler.server.zmq.zmq_receiver_thread import ZmqReceiverThread


class ZMQServerHandler(BaseServerHandler):
    def __init__(
        self,
        name=None,
        target_handler: logging.Handler = None,
        address: str = "tcp://127.0.0.1",
        level=logging.DEBUG,
    ):
        super(ZMQServerHandler, self).__init__(
            name=name, target_handler=target_handler, level=level
        )

        self._socket_type = zmq.PULL
        self._address = address
        self._socket = None

        self._start_background_processing()

    def _create_background_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseReceiverThread:
        return ZmqReceiverThread(
            name=thread_name,
            receiver_ready=processing_ready,
            handler=self,
            socket_type=self._socket_type,
            address=self._address,
        )

    def _start_background_thread(self):
        # Start zmq receiver
        thread = super(ZMQServerHandler, self)._start_background_thread()
        self._address = thread.address
        return thread

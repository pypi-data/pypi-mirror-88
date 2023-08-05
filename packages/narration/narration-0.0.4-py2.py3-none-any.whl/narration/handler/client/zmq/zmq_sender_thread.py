import threading
from queue import Queue

from narration.handler.client.base_sender_thread import BaseSenderThread
from narration.handler.common.zmq.zmq_socket import ZMQSocket
from narration.handler.common.socket.base_socket import BaseSocket
from narration.handler.common.zmq.zmq_resilient_socket import ZmqResilientSocket


class ZmqSenderThread(BaseSenderThread):
    def __init__(
        self,
        name: str = None,
        sender_ready: threading.Event = None,
        socket_type: object = None,
        address: str = None,
        queue: Queue = None,
        *args,
        **kwargs
    ):
        super(ZmqSenderThread, self).__init__(
            name=name,
            sender_ready=sender_ready,
            daemon=True,
            write_timeout=2.0,
            queue=queue,
            *args,
            **kwargs
        )

        self._socket_type = socket_type
        self._address = address

    def _create_socket(self) -> BaseSocket:
        zmq_socket = ZmqResilientSocket(self._socket_type, self._address, check=self._not_running)
        return ZMQSocket(zmq_socket=zmq_socket)

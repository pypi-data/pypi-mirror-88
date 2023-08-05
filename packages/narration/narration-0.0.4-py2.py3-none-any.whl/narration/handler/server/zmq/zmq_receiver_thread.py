import threading

from narration.handler.common.zmq.zmq_socket import ZMQSocket
from narration.handler.common.base_receiver_thread import BaseReceiverThread
from narration.handler.common.socket.base_socket import BaseSocket
from narration.handler.common.zmq.zmq_resilient_socket import ZmqResilientSocket


class ZmqReceiverThread(BaseReceiverThread):
    def __init__(
        self,
        name: str = None,
        receiver_ready: threading.Event = None,
        handler=None,
        socket_type: object = None,
        address: str = None,
        *args,
        **kwargs
    ):
        super(ZmqReceiverThread, self).__init__(
            name=name,
            receiver_ready=receiver_ready,
            handler=handler,
            daemon=True,
            read_timeout=2.0,
            *args,
            **kwargs
        )

        self._socket_type = socket_type
        self._address = address

    def _create_socket(self) -> BaseSocket:
        zmq_socket = ZmqResilientSocket(self._socket_type, self._address, check=self._not_running)
        return ZMQSocket(zmq_socket=zmq_socket)

    @property
    def address(self):
        return self._socket.address

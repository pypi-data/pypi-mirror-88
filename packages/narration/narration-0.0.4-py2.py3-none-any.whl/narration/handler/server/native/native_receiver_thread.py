import threading

from narration.handler.common.native.native_socket import NativeSocket
from narration.handler.common.base_receiver_thread import BaseReceiverThread
from narration.handler.common.socket.base_socket import BaseSocket


class NativeReceiverThread(BaseReceiverThread):
    def __init__(
        self,
        name: str = None,
        receiver_ready: threading.Event = None,
        handler=None,
        native_queue=None,
        *args,
        **kwargs
    ):
        super(NativeReceiverThread, self).__init__(
            name=name,
            receiver_ready=receiver_ready,
            handler=handler,
            daemon=True,
            read_timeout=2.0,
            *args,
            **kwargs
        )

        self._native_queue = native_queue

    def _create_socket(self) -> BaseSocket:
        return NativeSocket(native_queue=self._native_queue)

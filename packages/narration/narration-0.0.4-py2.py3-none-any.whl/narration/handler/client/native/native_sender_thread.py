import threading
from queue import Queue

from narration.handler.client.base_sender_thread import BaseSenderThread
from narration.handler.common.native.native_socket import NativeSocket
from narration.handler.common.socket.base_socket import BaseSocket


class NativeSenderThread(BaseSenderThread):
    def __init__(
        self,
        name: str = None,
        sender_ready: threading.Event = None,
        queue: Queue = None,
        native_queue: Queue = None,
        *args,
        **kwargs
    ):
        super(NativeSenderThread, self).__init__(
            name=name,
            sender_ready=sender_ready,
            daemon=True,
            write_timeout=2.0,
            queue=queue,
            *args,
            **kwargs
        )
        self._native_queue = native_queue

    def _create_socket(self) -> BaseSocket:
        return NativeSocket(native_queue=self._native_queue)

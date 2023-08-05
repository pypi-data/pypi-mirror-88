import threading
from queue import Queue

from narration.handler.client.base_client_handler import BaseClientHandler
from narration.handler.client.base_sender_thread import BaseSenderThread
from narration.handler.client.native.native_sender_thread import NativeSenderThread


class NativeClientHandler(BaseClientHandler):
    def __init__(self, name: str = None, queue=None, level=None):
        super(NativeClientHandler, self).__init__(name=name, queue=Queue(-1), level=level)
        self._native_queue = queue

        self._start_background_processing()

    def _create_background_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseSenderThread:
        return NativeSenderThread(
            name=thread_name,
            sender_ready=processing_ready,
            queue=self._queue,
            native_queue=self._native_queue,
        )

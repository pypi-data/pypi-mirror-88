import multiprocessing
import threading

from narration.handler.common.base_receiver_thread import BaseReceiverThread
from narration.handler.server.base_server_handler import BaseServerHandler
from narration.handler.server.native.native_receiver_thread import NativeReceiverThread


class NativeServerHandler(BaseServerHandler):
    def __init__(
        self,
        name=None,
        target_handler=None,
        queue=None,
        level=None,
    ):
        super(NativeServerHandler, self).__init__(
            name=name, target_handler=target_handler, level=target_handler.level
        )
        self._native_queue = queue

        self._start_background_processing()

    def _create_background_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseReceiverThread:
        return NativeReceiverThread(
            name=thread_name, receiver_ready=processing_ready, native_queue=self._native_queue
        )

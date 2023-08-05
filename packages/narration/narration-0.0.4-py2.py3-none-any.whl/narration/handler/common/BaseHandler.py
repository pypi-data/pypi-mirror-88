import logging
import threading
from enum import Enum

from narration.handler.common.base_receiver_thread import BaseReceiverThread
from narration.handler.common.utils import wait_for_event


class HandlerType(Enum):
    MAIN_PROCESS = "main"
    CLIENT_PROCESS = "client"


class BaseHandler(logging.Handler):
    def __init__(
        self,
        name: str = None,
        type: HandlerType = None,
        level=None,
        background_shutdown_timeout: float = 10.0,
    ):
        super(BaseHandler, self).__init__(level)
        self.name = name
        self._type = type
        self._thread = None
        self._background_shutdown_timeout = background_shutdown_timeout  # in seconds
        self._closed = False

    def _start_background_processing(self):
        self._thread = self._start_background_thread()

    def _stop_background_processing(self, timeout=None):
        self._stop_background_thread(timeout=timeout)

    def _create_background_thread(
        self, thread_name: str = None, processing_ready: threading.Event = None
    ) -> BaseReceiverThread:
        raise NotImplementedError()

    def _start_background_thread(self):
        processing_ready = threading.Event()

        name = f"background_{self._type.value}_{self.name}"
        thread = self._create_background_thread(thread_name=name, processing_ready=processing_ready)
        thread.start()

        wait_for_event(processing_ready, 60, thread.is_alive)

        return thread

    def _stop_background_thread(self, timeout=None):
        if self._thread is not None and self._thread.is_alive:
            self._thread.shutdown(timeout=timeout)
            # Wait until the thread stops
            self._thread.join(timeout=timeout)

    def close(self):
        if not self._closed:
            self._closed = True
            self._stop_background_processing(timeout=self._background_shutdown_timeout)
        super(BaseHandler, self).close()

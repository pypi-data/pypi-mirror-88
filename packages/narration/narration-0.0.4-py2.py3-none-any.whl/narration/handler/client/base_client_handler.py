from queue import Queue

from narration.handler.common.BaseHandler import BaseHandler, HandlerType


class BaseClientHandler(BaseHandler):
    def __init__(self, name: str = None, queue: Queue = None, level=None):
        super(BaseClientHandler, self).__init__(
            name=name, type=HandlerType.CLIENT_PROCESS, level=level
        )
        self._server_notified = False
        self._queue = queue

    def emit(self, record):
        try:
            self._queue.put(record, block=True)
        except BaseException:
            self.handleError(record)

    def close(self):
        # Wait for all queue items to be sent out
        self._queue.join()
        super(BaseClientHandler, self).close()

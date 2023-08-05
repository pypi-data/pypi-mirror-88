import logging

from narration.handler.common.BaseHandler import BaseHandler, HandlerType


class BaseServerHandler(BaseHandler):
    """The BaseServerHandler creates a connection between the main
    process and its children processes.

    The XXXXServerHandler is expected to be set up by the main process.

    """

    def __init__(
        self,
        name=None,
        target_handler: logging.Handler = None,
        level=logging.DEBUG,
    ):
        super(BaseServerHandler, self).__init__(
            name=name,
            type=HandlerType.MAIN_PROCESS,
            level=target_handler.level if target_handler is not None else level,
        )

        if target_handler is None:
            target_handler = logging.StreamHandler()
        self.target_handler = target_handler

        self.setFormatter(self.target_handler.formatter)
        self.filters = self.target_handler.filters

        self._client_count = 0
        self._raise_exception_on_server_closed_too_early = False

        self._receiver_thread = None
        self._address = None

    @property
    def address(self):
        return self._address

    def setFormatter(self, fmt):
        super(BaseServerHandler, self).setFormatter(fmt)
        self.target_handler.setFormatter(fmt)

    def emit(self, record):
        self.target_handler.handle(record)

    def close(self):
        super(BaseServerHandler, self).close()
        self.target_handler.flush()
        self.target_handler.close()

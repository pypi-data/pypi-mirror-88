from narration.handler.common.socket.bindfailedexception import BindFailedException
from narration.handler.common.socket.connectfailedexception import ConnectFailedException
from narration.handler.common.socket.readtimeoutexception import ReadTimeoutException
from narration.handler.common.socket.writetimeoutexception import WriteTimeoutException


class BaseSocket:
    def __init__(
        self,
    ):
        pass

    def bind(self):
        raise BindFailedException()

    def connect(self):
        raise ConnectFailedException()

    def read_record(self, op_timeout=None):
        raise ReadTimeoutException()

    def write_record(self, value, op_timeout=None):
        raise WriteTimeoutException()

    def close(self):
        raise NotImplementedError()

    @property
    def address(self):
        raise NotImplementedError()

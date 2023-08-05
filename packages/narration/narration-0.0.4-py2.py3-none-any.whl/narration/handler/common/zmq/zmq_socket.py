import errno

import zmq

from narration.handler.common.socket.base_socket import BaseSocket
from narration.handler.common.socket.readtimeoutexception import ReadTimeoutException
from narration.handler.common.socket.writetimeoutexception import WriteTimeoutException
from narration.handler.common.zmq.zmq_resilient_socket import ZmqResilientSocket


class ZMQSocket(BaseSocket):
    def __init__(self, zmq_socket: ZmqResilientSocket = None):
        self._zmq_socket = zmq_socket

    def bind(self):
        self._zmq_socket.bind()

    def connect(self):
        self._zmq_socket.connect()

    def read_record(self, op_timeout=None):
        try:
            return self._zmq_socket.recv_json(timeout=op_timeout)
        except zmq.ZMQError as error:
            if error.errno == errno.EAGAIN:
                raise ReadTimeoutException() from error

    def write_record(self, value, op_timeout=None):
        try:
            return self._zmq_socket.send_json(value, timeout=op_timeout)
        except zmq.ZMQError as error:
            raise WriteTimeoutException() from error

    def close(self):
        self._zmq_socket.close()

    @property
    def address(self):
        return self._zmq_socket.address

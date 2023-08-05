# https://gitlab.com/peick/starlog/-/blob/master/starlog/handlers/zmq_handler.py

import errno

import zmq
from narration.constants import NARRATION_DEBUG_HANDLER_SOCKET_ZMQ_PREFIX
from narration.handler.common.socket.base_socket import BaseSocket
from narration.debug.debug import get_debug_logger
from narration.handler.common.socket.readtimeoutexception import ReadTimeoutException
from narration.handler.common.utils import retry, RetryAbortedByCheck, requires_random_bind

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_SOCKET_ZMQ_PREFIX)


class BindFailedError(Exception):
    pass


class ZmqResilientSocket(BaseSocket):
    UNRECOVERABLE_ERRORS = [
        # "Permission denied"
        errno.EACCES,
    ]

    DEFAULT_SOCKET_OPTIONS = {
        # set recv timeout
        "RCVTIMEO": 1000,
        "LINGER": 0,
    }

    def __init__(
        self,
        socket_type,
        address,
        backoff_factor=2.0,
        tries=4,
        check=None,
        socket_options=DEFAULT_SOCKET_OPTIONS,
    ):
        # default: tries up to 2 minutes 15 seconds to bind / connect to
        # a socket
        self._socket_type = socket_type
        self._address = address

        self._context = None
        self._socket = None
        self._socket_options = socket_options

        self._retry_bind = retry(
            zmq.ZMQError,
            tries=tries,
            backoff_factor=backoff_factor,
            check=check,
            retry_log=self._log_bind_attempt,
        )

        self._retry_connect = retry(
            zmq.ZMQError,
            tries=tries,
            backoff_factor=backoff_factor,
            check=check,
            retry_log=self._log_bind_attempt,
        )

        self._poller = zmq.Poller()

    def _obtain_context(self):
        if self._context is None:
            self._context = zmq.Context()

        return self._context

    def _log_bind_attempt(self, _trial, last_trial=False):
        if last_trial:
            _log.error("bind to %s failed. Aborting.", self._address)
        else:
            _log.warning("bind to %s failed. Retrying", self._address)

    def _log_connect_attempt(self, _trial, last_trial=False):
        if last_trial:
            _log.error("connect to %s failed. Aborting.", self._address)
        else:
            _log.warning("connect to %s failed. Retrying.", self._address)

    def _poller_register(self, socket: zmq.Socket = None, flags: int = 0):
        self._poller.register(socket=socket, flags=flags)

    def _poller_unregister(self, socket: zmq.Socket = None):
        self._poller.unregister(socket=socket)

    def bind(self):
        bind_with_retries = self._retry_bind(self._bind)
        bind_with_retries()

    def _bind(self):
        poll_registered = False
        try:
            self.close_socket()
            context = self._obtain_context()
            self._socket = context.socket(self._socket_type)

            if requires_random_bind(self._address):
                port = self._socket.bind_to_random_port(self._address)
                self._address = "%s:%d" % (self._address, port)
            else:
                self._socket._bind_to_socket(self._address)

            self._set_socket_options()
            self._poller_register(socket=self._socket, flags=zmq.POLLIN | zmq.POLLOUT)
            poll_registered = True
        except zmq.ZMQError as error:
            if poll_registered and self._socket is not None:
                self._poller_unregister(socket=self._socket)

            if error.errno in self.UNRECOVERABLE_ERRORS:
                raise BindFailedError(str(error))

            raise

    def connect(self):
        connect_with_retries = self._retry_connect(self._connect)
        connect_with_retries()

    def _connect(self):
        self.close_socket()
        context = self._obtain_context()
        self._socket = context.socket(self._socket_type)
        self._socket.connect(self._address)
        self._poller_register(socket=self._socket, flags=zmq.POLLIN | zmq.POLLOUT)

    def _set_socket_options(self):
        if not self._socket_options:
            return

        for option, value in self._socket_options.items():
            setattr(self._socket, option, value)

    def recv_json(self, timeout=None):
        socks = dict(self._poller.poll(timeout=timeout))

        # Data can be read from socket
        if socks.get(self._socket) == zmq.POLLIN:
            try:
                return self._socket.recv_json()
            except zmq.ZMQError as error:
                if error.errno == errno.EAGAIN:
                    # read timeout
                    raise error

                self.bind()

        raise zmq.ZMQError(errno=errno.EAGAIN)

    def send_json(self, data, timeout=None):
        socks = dict(self._poller.poll(timeout=timeout))

        # Data can be written to socket
        if socks.get(self._socket) == zmq.POLLOUT:
            try:
                return self._socket.send_json(data)
            except zmq.ZMQError:
                self.connect()
                return self._socket.send_json(data)

        return None

    def close(self):
        """Close the zmq socket and destroy the zmq context."""
        self.close_socket()
        self.destroy_context()

    def destroy_context(self):
        """Destroy the zmq context."""
        if self._context is not None:
            if not self._context.closed:
                self._context.destroy()
            self._context = None

    def close_socket(self):
        """Close the zmq socket."""
        if self._socket is not None:
            if not self._socket.closed:
                self._socket.close()
                self._poller_unregister(socket=self._socket)
            self._socket = None

    @property
    def address(self):
        assert not requires_random_bind(self._address)
        return self._address

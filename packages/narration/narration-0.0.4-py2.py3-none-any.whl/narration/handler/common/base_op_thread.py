import sys
import traceback

from narration.handler.common.socket.base_socket import BaseSocket
from narration.handler.common.socket.bindfailedexception import BindFailedException
import threading
from enum import Enum
import time

from narration.constants import NARRATION_DEBUG_HANDLER_THREAD_PREFIX
from narration.debug.debug import get_debug_logger
from narration.handler.common.socket.connectfailedexception import ConnectFailedException

_log = get_debug_logger(NARRATION_DEBUG_HANDLER_THREAD_PREFIX)


class OpType(Enum):
    SEND = "send"
    RECEIVE = "receive"


class BaseOpThread(threading.Thread):
    def __init__(
        self,
        name=None,
        op_ready: threading.Event = None,
        daemon=None,
        op_timeout: float = 1.0,
        op_type: OpType = None,
        *args,
        **kwargs,
    ):
        super(BaseOpThread, self).__init__(None, None, name, *args, **kwargs, daemon=daemon)

        self._op_type = op_type
        self._op_ready = op_ready
        self._max_socket_op_timeout = op_timeout
        self._shutdown_timeout = None
        self._running = False

    def _not_running(self):
        return not self._running

    def _create_socket(self) -> BaseSocket:
        raise NotImplementedError()

    def _bind_to_socket(self, socket: BaseSocket = None) -> bool:
        """
        Bind to socket
        :param socket:
        :param op_ready:
        :return:
        """
        try:
            socket.bind()
            _log.debug(f"Socket binded for {self._op_type.value}ing")
            return True
        except BindFailedException:
            _log.warn(f"Socket binding failed for {self._op_type.value}ing", exc_info=1)
            return False

    def _unbind_from_socket(self, socket: BaseSocket = None, binded: bool = False):
        """
        Unbind from socket
        :param socket:
        :param binded:
        :return:
        """
        try:
            if binded:
                socket.close()
                _log.debug(f"Socket unbinded for {self._op_type.value}ing")
        except BaseException:
            _log.error(f"Socket unbind failed for {self._op_type.value}ing", exc_info=1)

    def _connect_to_socket(self, socket: BaseSocket = None) -> bool:
        try:
            socket.connect()
            _log.debug(f"Socket connected for {self._op_type.value}ing")
            return True
        except ConnectFailedException:
            _log.error(f"Socket connection failed for {self._op_type.value}ing", exc_info=1)
            return False

    def _disconnect_from_socket(self, socket: BaseSocket = None, connected: bool = None):
        try:
            if connected:
                socket.close()
                _log.debug(f"Socket disconnected for {self._op_type.value}ing")
        except BaseException:
            _log.error(f"Socket disconnection failed for {self._op_type.value}ing", exc_info=1)

    def _operate(self, socket: BaseSocket = None, op_timeout=None) -> bool:
        raise NotImplementedError()

    def run(self):
        self._running = True
        self._log_thread_started()

        default_socket_op_timeout = 0.2
        op_timeout = self._max_socket_op_timeout - (default_socket_op_timeout * 2.0)

        operating = False
        shutdown_elapsed = False
        dirty_shutdown = False

        # Create socket
        self._socket = socket = self._create_socket()
        binded = False
        connected = False
        if self._op_type == OpType.RECEIVE:
            # Bind to socket
            binded = self._bind_to_socket(socket=socket)
            # Thread running/ready only if socket is binded
            self._running = binded
            self._op_ready.set()
            self._op_ready = None
        elif self._op_type == OpType.SEND:
            # Connect to socket
            connected = self._connect_to_socket(socket=socket)
            # Thread running/ready only if socket is connected
            self._running = connected
            self._op_ready.set()
            self._op_ready = None
        else:
            self._running = False
            shutdown_elapsed = True

        shutdown_start_time = None
        shutdown_duration = 0
        # Case1: Thread is started => self._running == True
        # Case2: Thread is requested to stop. Thread will stop when:
        #        - no more reads are successful
        #        - or thread shutdown time has lapsed
        while (self._running) or operating or not shutdown_elapsed:
            try:
                operating = self._operate(socket=socket, op_timeout=op_timeout)
            except (KeyboardInterrupt, SystemExit):
                # Stop thread
                traceback.print_exc(file=sys.stderr)
                self._running = False
                self._shutdown_timeout = 0
                operating = False
                shutdown_elapsed = True
                dirty_shutdown = True
                break
            except BaseException as e:
                self._log_unexpected_exception_while_operating(e)

            if not self._running and not dirty_shutdown:
                if shutdown_start_time is None:
                    shutdown_start_time = time.perf_counter()

                shutdown_current_time = time.perf_counter()
                shutdown_duration = shutdown_current_time - shutdown_start_time
                shutdown_elapsed = shutdown_duration > self._shutdown_timeout

            self._log_thread_operating_status(
                self._running, operating, shutdown_elapsed, shutdown_duration
            )

        self._log_thread_operating_status(
            self._running, operating, shutdown_elapsed, shutdown_duration, dirty_shutdown
        )

        if self._op_type == OpType.RECEIVE:
            self._unbind_from_socket(socket=socket, binded=binded)
        elif self._op_type == OpType.SEND:
            self._disconnect_from_socket(socket=socket, connected=connected)

        self._log_thread_stopped()

    def _log_thread_operating_status(
        self, running, operating, shutdown_elpasped, shutdown_duration, dirty_shutdown=False
    ):
        _log.debug(
            f"{self._op_type.value}ing thread is running ({running}), operating logs ({operating}) and shutdown elapsed ({shutdown_elpasped} - {shutdown_duration}s - dirty shutdown {dirty_shutdown})"
        )

    def _log_unexpected_exception_while_operating(self, exception):
        _log.error(f"{self._op_type.value}ing thread unexpected error", exc_info=1)

    def _log_thread_started(self):
        _log.debug(f"{self._op_type.value}ing thread started")

    def _log_thread_stopped(self):
        _log.debug(f"{self._op_type.value}ing thread stopped")

    def shutdown(self, timeout=None):
        """Graceful shutdown."""
        self._running = False
        self._shutdown_timeout = timeout

import logging
import sys
import threading
import traceback
from time import sleep

from narration.handler.common.base_op_thread import BaseOpThread, OpType
from narration.handler.common.socket.optimeoutexception import OpTimeoutException
from narration.handler.common.socket.base_socket import BaseSocket
from narration.handler.common.socket.readtimeoutexception import ReadTimeoutException


class BaseReceiverThread(BaseOpThread):
    def __init__(
        self,
        name=None,
        receiver_ready: threading.Event = None,
        handler=None,
        daemon=None,
        read_timeout: float = 1.0,
        *args,
        **kwargs,
    ):
        super(BaseReceiverThread, self).__init__(
            name=name,
            op_ready=receiver_ready,
            daemon=daemon,
            op_timeout=read_timeout,
            op_type=OpType.RECEIVE,
            *args,
            **kwargs,
        )
        self._handler = handler

    def _operate(self, socket: BaseSocket = None, queue=None, op_timeout=None) -> bool:
        def has_read_record(record):
            return record is not None

        record = None
        try:
            raw_record = self._read_record_from_socket(socket=socket, op_timeout=op_timeout)
            if raw_record is not None:
                record = self._to_log_record(raw_record=raw_record)
                if record is not None and self._handler is not None:
                    self._handler.emit(record)
            return has_read_record(record)
        except ReadTimeoutException:
            return has_read_record(record)
        except (BrokenPipeError, EOFError):
            # Stop thread
            traceback.print_exc(file=sys.stderr)
            raise
        except BaseException as e:
            raise e

    def _to_log_record(self, raw_record: object = None) -> logging.LogRecord:
        return logging.makeLogRecord(raw_record) if raw_record is not None else None

    def _read_record_from_socket(self, socket: BaseSocket = None, op_timeout=0) -> object:
        return socket.read_record(op_timeout=op_timeout)

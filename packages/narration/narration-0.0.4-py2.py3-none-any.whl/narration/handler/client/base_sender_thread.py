import logging
import sys
import threading
import traceback
from queue import Queue

from narration.handler.common.base_op_thread import BaseOpThread, OpType
from narration.handler.common.zmq.serialization import record_to_dict
from narration.handler.common.socket.optimeoutexception import OpTimeoutException
from narration.handler.common.socket.base_socket import BaseSocket


class BaseSenderThread(BaseOpThread):
    def __init__(
        self,
        name=None,
        sender_ready: threading.Event = None,
        daemon=None,
        write_timeout: float = 1.0,
        queue: Queue = None,
        *args,
        **kwargs,
    ):
        super(BaseSenderThread, self).__init__(
            name=name,
            op_ready=sender_ready,
            daemon=daemon,
            op_timeout=write_timeout,
            op_type=OpType.SEND,
            *args,
            **kwargs,
        )
        self._queue = queue

    def _operate(self, socket: BaseSocket = None, op_timeout=None) -> bool:
        has_record = False
        record_written = False
        try:
            record = self._queue.get(block=True)
            has_record = True

            if record is not None:
                raw_record = self._to_log_record(record=record)
                if raw_record is not None:
                    self._write_record_on_socket(
                        socket=socket, raw_record=raw_record, op_timeout=op_timeout
                    )
                    record_written = True

            return record_written
        except OpTimeoutException:
            return record_written
        except (BrokenPipeError, EOFError):
            # Stop thread
            traceback.print_exc(file=sys.stderr)
            raise
        except BaseException as e:
            raise e
        finally:
            if has_record:
                self._queue.task_done()

    def _to_log_record(self, record: logging.LogRecord = None) -> object:
        return record_to_dict(record)

    def _write_record_on_socket(
        self, socket: BaseSocket = None, raw_record: object = None, op_timeout=0
    ):
        return socket.write_record(raw_record, op_timeout=op_timeout)

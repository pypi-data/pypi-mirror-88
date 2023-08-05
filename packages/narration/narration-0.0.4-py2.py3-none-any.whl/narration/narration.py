import logging
from typing import Dict

from narration.Backend import Backend
from narration.debug.debug import get_debug_logger
from narration.handler.client.native.native_client_handler import NativeClientHandler
from narration.constants import NARRATION_DEBUG_LOG_PREFIX, NARRATION_HANDLER_PREFIX
from narration.handler.client.zmq.zmq_client_handler import ZMQClientHandler
from narration.handler.server.base_server_handler import BaseServerHandler
from narration.handler.server.native.native_server_handler import NativeServerHandler
from narration.handler.server.zmq.zmq_server_handler import ZMQServerHandler

_log = get_debug_logger(NARRATION_DEBUG_LOG_PREFIX)


def _create_client_handler_factory(kwargs: Dict = {}):
    backend = kwargs.pop("backend")
    if backend is None:
        backend = Backend.DEFAULT

    if backend == Backend.NATIVE:
        return NativeClientHandler(**kwargs)
    elif backend == Backend.ZMQ:
        return ZMQClientHandler(**kwargs)


def _create_server_handler_factory(
    process_start_method: str = None, ctx=None, ctx_manager=None, **kwargs
):
    """
    Factory to create a multiprocessing aware logging handler instance
    :param kwargs: Keyword arguments:
    {
        name: str                      Native/ZMQ
        target_handler: Handler        Native/ZMQ
        queue: Queue (or similar),     Native
        server_address: str            ZMQ                 Eg: tcp://127.0.0.1 or tcp://127.0.0.1:9000
        level: int                     Native/ZMQ
        process_start_method: str             Native/ZMQ
    }
    :return ServerHandler, {} (Or None,None if no process starting method is identified nor no multiprocessing aware
    handler should be returned)
    """
    if None in [process_start_method, ctx_manager]:
        return None, {}

    backend = kwargs.pop("backend")
    if backend is None:
        backend = Backend.DEFAULT

    settings = {
        "level": kwargs.get("level", logging.DEBUG),
        "start_method": process_start_method,
        "backend": backend,
    }

    if backend == Backend.NATIVE:
        queue = kwargs.get("queue", None)
        queue_missing = queue is None
        if queue_missing:
            queue = ctx_manager.Queue(-1)
            kwargs.update(queue=queue)

        settings.update(queue=queue)
        return NativeServerHandler(**kwargs), settings
    elif backend == Backend.ZMQ:
        address = kwargs.get("address", None)
        address_missing = address is None
        if address_missing:
            # ZMQ will auto assign the port
            address = "tcp://127.0.0.1"

        kwargs.update(address=address)
        handler = ZMQServerHandler(**kwargs)
        settings.update(address=handler.address)

        return handler, settings


def setup_client_handlers(
    logger=None,
    handler_name_to_client_handler_settings: Dict = {},
    create_client_handler_factory=_create_client_handler_factory,
):
    # Add client handlers
    for (
        handler_name,
        client_handler_settings,
    ) in handler_name_to_client_handler_settings.items():
        start_method = client_handler_settings.get("start_method")
        client_handler_settings2 = {
            key: client_handler_settings[key]
            for key in client_handler_settings
            if key != "start_method"
        }
        client_handler_settings2.update(name=handler_name)
        handler = create_client_handler_factory(client_handler_settings2)
        handler.name = handler_name

        # Remove main process's logger's handlers for some start method
        if start_method in ["fork", "forkserver"]:
            logger.removeHandler(handler_name)

        # Add client handler
        logger.addHandler(handler)


def setup_server_handlers(
    logger=None,
    ctx=None,
    ctx_manager=None,
    backend=Backend.DEFAULT,
    create_server_handler_factory=_create_server_handler_factory,
):
    """Wraps a logger's handlers with ServerHandler instances.
       This utility function will setup the correct inter process communication to retrieve logs from child processes,
       regardless of the process start method used (fork, spawn, forkserver)

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    :return Tuple[ServerHandler's name, dict of client handler settings]. The dict must be considered opaque.
    """
    if logger is None:
        logger = logging.getLogger()

    settings = {}

    for i, orig_handler in enumerate(list(logger.handlers)):
        handler_name = (
            str(orig_handler.name) if orig_handler.name is not None else f"narration-handler-{i}"
        )
        kwargs = {
            "name": f"{NARRATION_HANDLER_PREFIX}{handler_name}",
            "target_handler": orig_handler,
            "level": orig_handler.level if orig_handler.level is not None else logging.DEBUG,
            "process_start_method": ctx.get_start_method(),
            "ctx": ctx,
            "ctx_manager": ctx_manager,
            "backend": backend,
        }
        server_handler, client_handler_settings = create_server_handler_factory(**kwargs)
        if server_handler is not None:
            logger.removeHandler(orig_handler)
            logger.addHandler(server_handler)
            settings[handler_name] = client_handler_settings

    return settings


def teardown_handlers(logger=None):
    """Unwraps a logger's handlers from their ServerHandler instances

    :param logger: Logger whose handlers to wrap. Default: Python root logger.
    """
    if logger is None:
        logger = logging.getLogger()

    for handler in logger.handlers:
        if isinstance(handler, BaseServerHandler):
            target_handler = handler.target_handler
            logger.removeHandler(handler)
            logger.addHandler(target_handler)

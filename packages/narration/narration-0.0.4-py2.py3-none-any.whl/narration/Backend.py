from enum import Enum


class Backend(Enum):
    NATIVE = "native"
    ZMQ = "zero-mq"
    DEFAULT = ZMQ

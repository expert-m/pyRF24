from .rf24 import RF24
from typing import Tuple, Union


class RF24NetworkHeader:
    def __init__(self, _to: int=None, _type: int=None) -> None: ...
    def to_string(self) -> str: ...

    @property
    def to_node(self) -> int: ...

    @property
    def type(self) -> int: ...

    @property
    def id(self) -> int: ...

    @property
    def from_node(self) -> int: ...

    @property
    def reserved(self) -> int: ...


class RF24Network:
    def __init__(self, _radio: RF24) -> None: ...
    def begin(self, _node_address: int) -> None: ...
    def is_address_valid(self, address: int) -> bool: ...
    def multicast(self, header: RF24NetworkHeader, buf: Union(bytes, bytearray), level: int=7) -> bool: ...
    def peek(self, header: RF24NetworkHeader) -> int: ...
    def peek(self, maxlen: int=None) -> Tuple(RF24NetworkHeader, bytearray): ...
    def read(self, maxlen: int=None) -> Tuple(RF24NetworkHeader, bytearray): ...
    def set_multicast_level(self, level: int) -> None: ...
    def update(self) -> int: ...
    def write(self, header: RF24NetworkHeader, buf: Union(bytearray, bytes)) -> bool: ...

    @property
    def multicast_relay(self) -> bool: ...

    @property
    def multicast_level(self) -> int: ...

    @property
    def network_flags(self) -> int: ...

    @property
    def node_address(self) -> int: ...

    @property
    def parent(self) -> int: ...

    @property
    def route_timeout(self) -> int: ...

    @property
    def tx_timeout(self, timeout: int) -> int: ...

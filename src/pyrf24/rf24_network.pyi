# pylint: skip-file
from typing import Tuple, Union, List, overload
from .rf24 import RF24

MAX_USER_DEFINED_HEADER_TYPE: int = 127
MAX_PAYLOAD_SIZE: int = 144
NETWORK_ADDR_RESPONSE: int = 128
NETWORK_PING: int = 130
EXTERNAL_DATA_TYPE: int = 131
NETWORK_FIRST_FRAGMENT: int = 148
NETWORK_MORE_FRAGMENTS: int = 149
NETWORK_LAST_FRAGMENT: int = 150
NETWORK_ACK: int = 193
NETWORK_POLL: int = 194
NETWORK_REQ_ADDRESS: int = 195
FLAG_FAST_FRAG: int = 4
FLAG_NO_POLL: int = 8

class RF24NetworkHeader:
    @overload
    def __init__(self, to_node: int, type: int = 0) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def to_string(self) -> str: ...
    @property
    def to_node(self) -> int: ...
    @to_node.setter
    def to_node(self, value: int): ...
    @property
    def type(self) -> int: ...
    @type.setter
    def type(self, value: int): ...
    @property
    def id(self) -> int: ...
    @id.setter
    def id(self, value: int): ...
    @property
    def from_node(self) -> int: ...
    @from_node.setter
    def from_node(self, value: int): ...
    @property
    def reserved(self) -> int: ...
    @reserved.setter
    def reserved(self, value: int): ...
    @property
    def next_id(self) -> int: ...

# RF24NetworkFrame is not exposed as is not needed
# class RF24NetworkFrame:
#     def __init__(
#         self, header: RF24NetworkHeader = None, message: Union[bytes, bytearray] = None
#     ): ...
#     @property
#     def header(self) -> RF24NetworkHeader: ...
#     @header.setter
#     def header(self, head: RF24NetworkHeader): ...
#     @property
#     def message_buffer(self) -> bytearray: ...
#     @message_buffer.setter
#     def message_buffer(self, message: Union[bytes, bytearray]): ...
#     @property
#     def message_size(self) -> int: ...

class RF24Network:
    def __init__(self, radio: RF24) -> None: ...
    @overload
    def begin(self, node_address: int) -> None: ...
    @overload
    def begin(self, channel:int, node_address: int) -> None: ...
    def is_address_valid(self, address: int) -> bool: ...
    def is_valid_address(self, address: int) -> bool: ...
    def multicast(
        self, header: RF24NetworkHeader, buf: Union[bytes, bytearray], level: int = 7
    ) -> bool: ...
    def multicastLevel(self, level: int) -> None: ...
    @overload
    def peek(self, header: RF24NetworkHeader) -> int: ...
    @overload
    def peek(self, maxlen: int = None) -> Tuple[RF24NetworkHeader, bytearray]: ...
    def read(self, maxlen: int = None) -> Tuple[RF24NetworkHeader, bytearray]: ...
    def set_multicast_level(self, level: int) -> None: ...
    def update(self) -> int: ...
    def available(self) -> int: ...
    def write(
        self, header: RF24NetworkHeader, buf: Union[bytearray, bytes]
    ) -> bool: ...
    @property
    def multicast_relay(self) -> bool: ...
    @multicast_relay.setter
    def multicast_relay(self, enable: bool): ...
    @property
    def multicastRelay(self) -> bool: ...
    @multicastRelay.setter
    def multicastRelay(self, enable: bool): ...
    @property
    def multicast_level(self) -> int: ...
    @multicast_level.setter
    def multicast_level(self, level: int): ...
    @property
    def network_flags(self) -> int: ...
    @network_flags.setter
    def network_flags(self, flags: int): ...
    @property
    def networkFlags(self) -> int: ...
    @networkFlags.setter
    def networkFlags(self, flags: int): ...
    @property
    def node_address(self) -> int: ...
    @node_address.setter
    def node_address(self, address: int): ...
    @property
    def parent(self) -> int: ...
    @property
    def return_sys_msgs(self) -> bool: ...
    @return_sys_msgs.setter
    def return_sys_msgs(self, enable: bool): ...
    @property
    def returnSysMsgs(self) -> bool: ...
    @returnSysMsgs.setter
    def returnSysMsgs(self, enable: bool): ...
    @property
    def route_timeout(self) -> int: ...
    @route_timeout.setter
    def route_timeout(self, timeout: int): ...
    @property
    def routeTimeout(self) -> int: ...
    @routeTimeout.setter
    def routeTimeout(self, timeout: int): ...
    @property
    def tx_timeout(self) -> int: ...
    @tx_timeout.setter
    def tx_timeout(self, timeout: int) -> int: ...
    @property
    def txTimeout(self) -> int: ...
    @txTimeout.setter
    def txTimeout(self, timeout: int) -> int: ...
    # @property
    # def external_queue(self) -> List[RF24NetworkFrame]: ...
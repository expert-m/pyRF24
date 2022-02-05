"""
An all-purpose example of using the nRF24L01 transceiver in a network of nodes.
"""
import sys
import time
import struct
from pyrf24 import (
    RF24,
    RF24Network,
    RF24NetworkHeader,  # only need to construct frame headers for RF24Network.write()
    RF24Mesh,
    MAX_PAYLOAD_SIZE,
    MESH_DEFAULT_ADDRESS,
    RF24_PA_LOW,
)


radio = RF24(22, 0)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

print(sys.argv[0])
IS_MESH = (
    (
        input("Would you like to run as a mesh network node (y/n)? Defaults to 'Y' ")
        or "Y"
    )
    .upper()
    .startswith("Y")
)

# to use different addresses on a set of radios, we need a variable to
# uniquely identify this radio.
THIS_NODE = 0
print(
    "Remember, the master node always uses `0` as the node_address and node_id."
    "\nWhich node is this? Enter",
    end=" ",
)
if IS_MESH:
    # node_id must be less than 255
    THIS_NODE = int(input("a unique int. Defaults to '0' ") or "0") & 0xFF
else:
    # logical node_address is in octal
    THIS_NODE = int(input("an octal int. Defaults to '0' ") or "0", 8)

if not radio.begin():
    raise OSError("radio hardware not responding")
if IS_MESH:
    mesh.node_id = THIS_NODE
    # RF24Mesh C++ library uses channel 97 by default
    if not mesh.begin():
        raise OSError("could not connect to mesh network")
else:
    # C++ examples use channel 90 for RF24Network library
    radio.channel = 90
    network.begin(THIS_NODE)

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity
radio.pa_level = RF24_PA_LOW

# This example covers fragmented payloads also. Set a sentinel for readability.
MAX_FRAG_SIZE = 24

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our number of the payloads sent
packets_sent = [0]

if THIS_NODE:  # if this node is not the network master node
    if IS_MESH:  # mesh nodes need to bond with the master node
        print("assigned address:", oct(mesh.mesh_address))
else:
    print("Acting as network master node.")


def idle(timeout: int = 30):
    """Listen for any payloads and print the transaction

    :param int timeout: The number of seconds to wait (with no transmission)
        until exiting function.
    """
    print("idling for", timeout, "seconds")
    start_timer = time.monotonic()
    while (time.monotonic() - start_timer) < timeout:
        network.update()  # keep the network layer current
        if THIS_NODE and IS_MESH:
            mesh.dhcp()
        while network.available():
            start_timer = time.monotonic()  # reset timer
            header, payload = network.read()
            payload_len = len(payload)
            print("Received payload", end=" ")
            # TMRh20 examples only use 1 or 2 long ints as small messages
            if payload_len < MAX_FRAG_SIZE and payload_len % 4 == 0:
                # if not a large fragmented message and multiple of 4 bytes
                fmt = "<" + "L" * int(payload_len / 4)
                print(struct.unpack(fmt, payload), end=" ")
            print(header.to_string(), "length", payload_len)


def emit(
    node: int = not THIS_NODE, frag: bool = False, count: int = 5, interval: int = 1
):
    """Transmits 1 (or 2) integers or a large buffer

    :param int node: The target node for network transmissions.
        If using RF24Mesh, this is a unique node_id.
        If using RF24Network, this is the node's logical address.
    :param bool frag: Only use fragmented messages?
    :param int count: The max number of messages to transmit.
    :param int interval: time (in seconds) between transmitting messages.
    """
    failures = 0
    while failures < 6 and count:
        idle(interval)  # idle till its time to emit
        count -= 1
        packets_sent[0] += 1
        # TMRh20's RF24Mesh examples use 1 long int containing a timestamp (in ms)
        message = struct.pack("<L", int(time.monotonic() * 1000))
        if frag:
            message = bytes(range((packets_sent[0] + MAX_FRAG_SIZE) % MAX_PAYLOAD_SIZE))
        elif not IS_MESH:  # if using RF24Network
            # TMRh20's RF24Network examples use 2 long ints, so add another
            message += struct.pack("<L", packets_sent[0])
        result = False
        start = time.monotonic_ns()
        if IS_MESH:  # write() is a little different for RF24Mesh vs RF24Network
            result = mesh.write(message, ord("M"), node)
        else:
            result = network.write(RF24NetworkHeader(node, ord("T")), message)
        end = time.monotonic_ns()
        failures += not result
        print(
            f"Sending {packets_sent[0]} (len {len(message)})...",
            "ok." if result else "failed.",
            f"Transmission took {int((end - start) / 1000000)} ms",
        )


def set_role():
    """Set the role using stdin stream. Timeout arg for idle() can be
    specified using a space delimiter (e.g. 'I 10' calls `idle(10)`)
    """
    prompt = (
        "*** Enter 'I' for idle role.\n"
        "*** Enter 'E <node number>' for emitter role.\n"
        "*** Enter 'E <node number> 1' to emit fragmented messages.\n"
    )
    if IS_MESH:
        if mesh.mesh_address == MESH_DEFAULT_ADDRESS:
            prompt += "!!! Mesh node not connected.\n"
        prompt += "*** Enter 'C' to connect to to mesh master node.\n"
    user_input = input(prompt + "*** Enter 'Q' to quit example.\n") or "?"
    user_input = user_input.split()
    if user_input[0].upper().startswith("C") and IS_MESH:
        print("Connecting to mesh network...", end=" ")
        result = mesh.renew_address(*[int(x) for x in user_input[1:2]])
        result = result != MESH_DEFAULT_ADDRESS
        print(("assigned address " + oct(mesh.mesh_address)) if result else "failed.")
        return True
    if user_input[0].upper().startswith("I"):
        idle(*[int(x) for x in user_input[1:2]])
        return True
    if user_input[0].upper().startswith("E"):
        emit(*[int(x) for x in user_input[1:5]])
        return True
    if user_input[0].upper().startswith("Q"):
        radio.power = False
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return set_role()


if __name__ == "__main__":

    try:
        while set_role():
            pass  # continue example until 'Q' is entered
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Powering down radio...")
        radio.power = False
elif IS_MESH and mesh.mesh_address != MESH_DEFAULT_ADDRESS:
    print("    Run emit(<node number>) to transmit.")
    print("    Run idle() to receive or forward messages in the network.")
    print("    Pass keyword arg `frag=True` to emit() fragmented messages.")

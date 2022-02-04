#!/usr/bin/env python3
"""
Simplest RF24Mesh example that transmits a time stamp (in milliseconds) 1 per second.
"""
import time
import struct
from pyrf24 import RF24, RF24Network, RF24Mesh

start = time.monotonic()


def millis():
    """:Returns: Delta time since started example in milliseconds. Wraps value around
    the width of a ``long`` integer."""
    return int((time.monotonic() - start) * 1000) % (2**32)


radio = RF24(22, 0)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)

mesh.node_id = 4
print("starting nodeID", mesh.node_id)
if not mesh.begin():
    raise OSError("failed to initialize radio or could not connect to mesh")
radio.print_pretty_details()

TIMER = 0

try:
    while True:
        # Call mesh.update to keep the network updated
        mesh.update()

        if (millis() - TIMER) >= 1000:
            TIMER = millis()

            if not mesh.write(struct.pack("L", TIMER), ord("M")):
                # If a write fails, check connectivity to the mesh network
                if not mesh.check_connection():
                    # The address could be refreshed per a specified timeframe
                    # or only when sequential writes fail, etc.
                    print("Renewing Address")
                    mesh.renew_address()
                else:
                    print("Send fail, Test OK")
            else:
                print("Send OK:", TIMER)
        time.sleep(0.001)  # delay 1 ms
except KeyboardInterrupt:
    radio.power = False  # power radio down before exiting

"""
Example of using the rf24_mesh module to operate the nRF24L01 transceiver as
a Mesh network master node.
"""
from pyrf24 import RF24, RF24Network, RF24Mesh


radio = RF24(22, 0)
network = RF24Network(radio)
mesh = RF24Mesh(radio, network)
mesh.begin(0)
radio.print_pretty_details()


while True:
    mesh.update()
    mesh.dhcp()

    while network.available():
        header, payload = network.read()
        print(f"Received message {header.to_string()}")

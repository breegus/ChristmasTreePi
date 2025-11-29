import paho.mqtt.client as mqtt_client
from uuid import getnode as get_mac

class HomeAssistant:
    def __init__(self, hostname="") -> None:
        self.hostname = hostname
        if not self.hostname:
            self.hostname = str(hex(get_mac()))

        self.isConnected = False

        self._mqtt = mqtt_client.Client(client_id=self.hostname)

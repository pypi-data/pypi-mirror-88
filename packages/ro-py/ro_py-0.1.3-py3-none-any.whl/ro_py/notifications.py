from ro_py.utilities.caseconvert import to_snake_case
from signalrcore.hub_connection_builder import HubConnectionBuilder
from urllib.parse import quote
import logging
import json


class Notification:
    def __init__(self, notification_data):
        self.identifier = notification_data["C"]
        self.hub = notification_data["M"][0]["H"]
        self.type = notification_data["M"][0]["M"]
        self.atype = notification_data["M"][0]["A"][0]
        self.raw_data = json.loads(notification_data["M"][0]["A"][1])
        self.data = {}
        for key, value in self.raw_data.items():
            self.data[to_snake_case(key)] = value


class NotificationReceiver:
    def __init__(self, requests, on_open, on_close, on_error):
        self.requests = requests

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error

        self.roblosecurity = self.requests.cookies[".ROBLOSECURITY"]
        self.negotiate_request = self.requests.get(
            url="https://realtime.roblox.com/notifications/negotiate"
                "?clientProtocol=1.5"
                "&connectionData=%5B%7B%22name%22%3A%22usernotificationhub%22%7D%5D",
            cookies={
                ".ROBLOSECURITY": self.roblosecurity
            }
        )
        self.wss_url = f"wss://realtime.roblox.com/notifications?transport=websockets" \
                       f"&connectionToken={quote(self.negotiate_request.json()['ConnectionToken'])}" \
                       f"&clientProtocol=1.5&connectionData=%5B%7B%22name%22%3A%22usernotificationhub%22%7D%5D"
        self.connection = HubConnectionBuilder()
        self.connection.with_url(
            self.wss_url,
            options={
                "headers": {
                    "Cookie": f".ROBLOSECURITY={self.roblosecurity};"
                },
                "skip_negotiation": False
            }
        )
        self.connection.configure_logging(logging.DEBUG)
        self.connection.with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

        self.connection.on_open(self.on_open)
        self.connection.on_close(self.on_close)
        self.connection.on_error(self.on_error)
        self.connection.on("UserNotificationHub", lambda b: print(b))
        self.connection.start()

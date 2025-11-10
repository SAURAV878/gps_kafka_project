from http.server import BaseHTTPRequestHandler
import json
import paho.mqtt.client as mqtt
from http.server import HTTPServer

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "rider"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
print("MQTT client is connected to HTTP server")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "api":
            length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(length)
            data = json.loads(body)

            mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
            print("Forwarded to Mqtt:", data)

            self.send_response(200)
            self.send_header("Content-Type", "appication/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "sent"}).encode())
        else:
            self.send_response(404)
            self.end_headers()    
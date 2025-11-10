from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "rider"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
print("MQTT client is connected to HTTP server")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


    def do_POST(self):
        # Correct path check
        if self.path == "/api/gps":
            length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(length)
            data = json.loads(body)

            # Publish to MQTT
            mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
            print("Forwarded to MQTT:", data)

            # Reply to browser
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "sent"}).encode())
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(" HTTP server running on http://127.0.0.1:8080")
    httpd.serve_forever()
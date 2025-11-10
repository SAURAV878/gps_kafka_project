import paho.mqtt.client as mqtt
import json 
import time 

client = mqtt.Client()
client.connect("localhost", 1883)
print("Connected to MQTT broker ")

gps_data = {
    "device_id":"rider_01",
    "latitude":  27.361,
    "longitude": 85.312,
    "timestamp": time.time()
}

message = json.dumps(gps_data)

topic = "rider"
client.publish(topic, message)
print(f"Published to '{topic}': {message}")

client.disconnect()
print("Disconnected from broker")
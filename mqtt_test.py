import paho.mqtt.client as mqtt 

client = mqtt.Client()
client.connect("localhost", 1883)
print("Connected to MQTT Broker")

topic = "rider"
message = "Hello from Python Mqtt"
client.publish(topic, message)
print(f"Published to '{topic}': {message}")

client.disconnect()
print("Disconnected from broker")
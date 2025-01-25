import random
import time
import json
from paho.mqtt import client as mqtt_client
from paho import mqtt


broker = "d24b7f97192047f6a48f86f35984e6eb.s1.eu.hivemq.cloud"
port = 8883
topic_read = "topic/pattern"
topic_publish = "topic"
# Generate a Client ID with the publish prefix.
client_id = f"publish-{random.randint(0, 1000)}"
username = "test2"
password = "Tymbark123@"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.tls_set(tls_version = mqtt.client.ssl.PROTOCOL_TLS)
    client.connect(broker, port)
    return client


def set_test(client: mqtt_client):
    client.publish(topic, f"Yeah, buddy lightweight.")


def event_handler(command: str, client: mqtt_client):
    if command == "Is it working?":
        set_test(client)
    else:
        command = ''.join(('0x',command))
        client.publish(topic, command)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        commmand = msg.payload.decode()
        print(f"Received `{commmand}` from `{msg.topic}` topic")
        event_handler(commmand, client)
    client.subscribe(topic)
    client.on_message = on_message


def run(client: mqtt_client):
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    client = connect_mqtt()
    run(client)

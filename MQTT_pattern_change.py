import random
import time
import json
from RIS_usb_class import RIS_usb
from paho.mqtt import client as mqtt_client
from paho import mqtt


broker = "d24b7f97192047f6a48f86f35984e6eb.s1.eu.hivemq.cloud"
port = 1883
topic_pattern = "topic_pattern/pattern"
topic_com = "topic_pattern/command"
# Generate a Client ID with the publish prefix.
client_id = f"publish-{random.randint(0, 1000)}"


try:
    with open("config.json") as config_f:
        config = json.load(config_f)
        ris_ports = config["RIS_PORTS"]
        config_f.close()
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def check_voltage(RIS_list: list, client: mqtt_client):
    for ris in RIS_list:
        voltage = ris.read_EXT_voltage()
        client.publish(topic_pattern, f"{ris.id} : {voltage}")


def check_pattern(RIS_list: list, client: mqtt_client):
    for ris in RIS_list:
        pattern = ris.read_pattern()
        client.publish(topic_pattern, f"{ris.id} : {pattern}")


def set_pattern_with_ack(RIS_list: list, client: mqtt_client, commmand: str):
    for ris in RIS_list:
        ris.set_pattern(commmand)
        pattern = ris.read_pattern()
        client.publish(topic_pattern, f"{ris.id} : {pattern}")


def event_handler(commmand: str, RIS_list: list, client: mqtt_client):
    if commmand == "?Vext":
        check_voltage(RIS_list, client)
    elif commmand == "?Pattern":
        check_pattern(RIS_list, client)
    else:
        command = "".join(("0x", command))
        print(command)
        set_pattern_with_ack(commmand)


def subscribe(client: mqtt_client, RIS_list: list):
    def on_message(client, userdata, msg):
        commmand = msg.payload.decode()
        print(f"Received `{commmand}` from `{msg.topic_pattern}` topic_pattern")
        event_handler(commmand, RIS_list, client)

    client.subscribe(topic_com)
    client.on_message = on_message


def run(RIS_list: list, client: mqtt_client):
    subscribe(client, RIS_list)
    check_pattern(RIS_list, client)
    client.loop_forever()


def ris_usb_init() -> list:
    RIS_list = []
    id = 0
    for port in ris_ports:
        RIS_list.append(RIS_usb(port, id))
        id += 1
    for ris in RIS_list:
        ris.reset()
    return RIS_list


if __name__ == "__main__":
    RIS_list = ris_usb_init()
    client = connect_mqtt()
    run()

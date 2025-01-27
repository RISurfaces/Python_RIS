import random
import time
import json
from RIS_usb_class import RIS_usb
from paho.mqtt import client as mqtt_client
from paho import mqtt


broker = "192.168.8.213"
port = 1883
topic_pattern = "topic/pattern"
topic_com = "topic/command"
topic_params = "topic/Params"
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


def check_RIS_metadata(RIS_list: list, client: mqtt_client):
    for ris in RIS_list:
        voltage = ris.read_EXT_voltage()
        client.publish(topic_params, f"Voltage: {ris.id} : {voltage}")
        pattern = ris.read_Serial_no()
        client.publish(topic_params, f"Serial: {ris.id} : {pattern}")
        pattern = ris.read_pattern()
        if pattern != None:
            val = pattern[3:-1]
            client.publish(topic_pattern, f"{val}")


def set_pattern_with_ack(RIS_list: list, client: mqtt_client, val: str):
    for ris in RIS_list:
        ris.set_pattern(val)
        time.sleep(1)
        pattern = ris.read_pattern()
        if pattern != None:
            val = pattern[3:-1]
            client.publish(topic_pattern, f"{val}")


def check_RIS_pattern(RIS_list: list, client: mqtt_client):
    pattern = RIS_list[0].read_pattern()
    if pattern != None:
        val = pattern[3:-1]
        client.publish(topic_pattern, f"{val}")


def event_handler(command: str, RIS_list: list, client: mqtt_client):
    if command == "?Params":
        check_RIS_metadata(RIS_list, client)
    elif command == "?Pattern":
        check_RIS_pattern(RIS_list, client)
    else:
        val = "".join(("0x", command))
        set_pattern_with_ack(RIS_list, client, val)


def subscribe(client: mqtt_client, RIS_list: list):
    def on_message(client, userdata, msg):
        command = msg.payload.decode()
        event_handler(command, RIS_list, client)
    client.subscribe(topic_com)
    client.on_message = on_message


def run(RIS_list: list, client: mqtt_client):
    subscribe(client, RIS_list)
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
    run(RIS_list, client)

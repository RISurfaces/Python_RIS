import RIS_ble_class as RIS_ble
from RsSmw import *
import asyncio
from bleak import *
import json
import time

try:
    with open("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq = config["START_FREQ"]
        end_freq = config["END_FREQ"]
        step_freq = config["STEP_FREQ"]
        span = config["SPAN"]
        analyzer_mode = config["ANALYZER_MODE"]
        revlevel = config["REVLEVEL"]
        rbw = config["RBW"]
        ris_ports = config["RIS_PORTS"]
        generator_amplitude = config["GENERATOR_AMPLITUDE"]
        pattern_for_negation = config["ID_FOR_NEGATION"]
        RIS_SET_TIME_BLE = config["RIS_SET_TIME_BLE"]
        WRITE_UUID = config["WRITE_UUID"]
        READ_UUID = config["READ_UUID"]
        DESCRIPTOR_NUMBER = config["DESCRIPTOR_NUMBER"]
        # More modes will be add later.
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else:
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()

try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
while True:
    input("Potwierdz start pomiaru: ")
    ris_ble = RIS_ble.RIS_ble("A-3163CA", 0)
    response = asyncio.run(ris_ble.connect_multiple_patterns())
    print(response)

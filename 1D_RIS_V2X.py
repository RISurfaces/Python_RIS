import analyzer
import generator
from RIS_usb_class import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
import datetime

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


def set_pattern_ris(pattern: str, ris: RIS_usb):
    if ris.id % 2 == 1 and int(pattern["ID"]) in pattern_for_negation:
        ris_pattern = ris.ris_pattern_negation(pattern["HEX"])
    else:
        ris_pattern = pattern["HEX"]
    ris.set_pattern(ris_pattern)
    return True


def pattern_loop(freq, RIS_list: list, measure_point: str):
    for pattern in patterns_data:
        for ris in RIS_list:
            is_pattern_set = set_pattern_ris(pattern, ris)
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        with open(f"V2X_12_05_25_{measure_point}.csv", "a+") as file:
            current_time = datetime.datetime.now()
            file.write(
                pattern["ID"] + ";" + str(current_time)
            )  # Write information about pattern information
            file.write(";")
            file.close()  # CLose the file
            # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer.trace_get(f"V2X_12_05_25_{measure_point}.csv")


def freq_loop(freq_data: list, RIS_list: list, measure_point: str):
    for freq in freq_data:
        generator.meas_prep(
            True, generator_mode, generator_amplitude, freq
        )  # True means that generator is set up an generate something.
        pattern_loop(freq, RIS_list, measure_point)


def ris_usb_init() -> list:
    RIS_list = []
    id = 0
    for port in ris_ports:
        print(port, " ", id)
        RIS_list.append(RIS_usb(port, id))
        id += 1
    for ris in RIS_list:
        ris.reset()
    return RIS_list


if __name__ == "__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        RIS_list = ris_usb_init()
        measure_point = input("Podaj punkt pomiarowy: ")
        print(type(measure_point))
        freq_data = np.arange(start_freq, end_freq + step_freq, step_freq)
        freq_loop(freq_data, RIS_list, measure_point)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()

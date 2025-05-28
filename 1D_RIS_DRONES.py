import analyzer
import generator
from RIS_usb_class import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
import datetime
import serial

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
        crane_pmw = config["CRANE_PWM"]
        crane_port = config["CRANE_PORT"]
        crane_time_between_measures = config["CRANE_TIME_BETWEEN_MEASURES"]
        try:
            serial_crane = serial.Serial(crane_port)
        except serial.SerialException:
            print("[SERIAL_ERROR] Check is crane port in config file is corret.")
            exit()
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
            serial_crane.write(crane_pmw) # send information about speed of crane
        while serial_crane.read() != "Done":
            analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
            time.sleep(crane_time_between_measures)
            with open(trace_file, "a+") as file:
                current_time = datetime.datetime.now()
                file.write(
                    pattern["ID"] + ";" + str(current_time)
                )
                file.write(";")
                file.close()  # CLose the file
                analyzer.trace_get(trace_file)


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
        freq_data = np.arange(start_freq, end_freq + step_freq, step_freq)
        freq_loop(freq_data, RIS_list)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()

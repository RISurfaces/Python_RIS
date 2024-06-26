import analyzer
import generator
from RIS_usb_class import RIS_usb
import json
import numpy as np
from RsSmw import *
import time

try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        ris_ports = config["RIS_PORTS"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
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
    with open("RIS_patterns_second.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()

def ris_pattern_negation(ris_pattern : str) -> str:
    ris_pattern = int(ris_pattern,16)
    ris_pattern = ~ris_pattern & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    ris_pattern = hex(ris_pattern)
    ris_pattern = str(ris_pattern)
    no_of_zero_to_add = 66 - len(ris_pattern)
    for i in range(no_of_zero_to_add):
        ris_pattern = ris_pattern[:2] + '0' + ris_pattern [2:]
    return ris_pattern

def pattern_loop(freq, RIS_list : list):
    for pattern in patterns_data:
        for ris in RIS_list:
            if int(pattern["ID"]) in pattern_for_negation:
                if ris.id == 0:
                    ris_pattern = pattern["HEX"]
                    ris.set_pattern(ris_pattern)
                else:
                    ris_pattern = ris_pattern_negation(pattern["HEX"])
                    ris.set_pattern(ris_pattern)
            else:
                ris.set_pattern(pattern[["HEX"]])
            ris.set_pattern(pattern["HEX"])
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        with open(trace_file, 'a+') as file:
            file.write(str(ris.id)+";"+pattern["ID"]+";"+pattern["DESC"])  # Write information about pattern information
            file.write(";")
            file.close()  # CLose the file
            # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        time.sleep(0.1)
        analyzer.trace_get()

def freq_loop(freq_data : list, RIS_list : list):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq, RIS_list)

def ris_usb_init() -> list:
    RIS_list = []
    id = 0
    for port in ris_ports:
        RIS_list.append(RIS_usb(port, id))
        id+=1
    for ris in RIS_list:
        ris.reset()
    return RIS_list

if __name__=="__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        RIS_list = ris_usb_init()
        freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
        freq_loop(freq_data, RIS_list)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()

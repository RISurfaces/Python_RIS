import analyzer
import generator
import RIS_usb
import remote_head
import json
import numpy as np
from RsSmw import *
import time
import RIS_usb

try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
        azimuth_step=config["AZIMUTH_STEP"]
        azimuth_no_angles = config["AZIMUTH_NO_ANGLES"]
        elevation_step=config["ELEVATION_STEP"]
        elevation_start_position = config["ELEVATION_START_STEPS"]  
        step_resolution = config["STEP_RESOLUTION"]
        elevation_no_angles = config["ELEVATION_NO_ANGLES"]
        step_resolution = config["STEP_RESOLUTION"]
        pattern_for_negation = config["ID_FOR_NEGATION"]
        ris_ports = config["RIS_PORTS"]
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
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
    
def count_angle(step : int) -> str:
    angle = step*1/(step_resolution)*1.8
    return str(float(angle))

def prepare_freq() -> list:
    if start_freq != end_freq:   
        freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    else:
        freq_data = [start_freq]
    return freq_data

def set_pattern_ris(pattern : str, ris : RIS_usb):
        if ris.id % 2 == 1 and int(pattern["ID"]) in pattern_for_negation:
            ris_pattern = ris.ris_pattern_negation(pattern["HEX"])
        else:
            ris_pattern = pattern["HEX"]
        ris.set_pattern(ris_pattern)
        return True

def pattern_loop(freq, azimuth_angle : str, elevation_angle : str, RIS_list : list):
    for pattern in patterns_data:
        for ris in RIS_list:
           is_pattern_set = set_pattern_ris(pattern, ris)
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        with open(trace_file, 'a+') as file:
            file.write(round(azimuth_angle,2)+";"+round(elevation_angle, 2)+";"+pattern["ID"]+";")  # Write information about pattern and angle
            file.write(";")
            file.close()  # CLose the file
            #RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        time.sleep(0.1)
        analyzer.trace_get()

def freq_loop(freq_data : list, azimuth_angle : str, elevation_angle :str,  RIS_list : list):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq, azimuth_angle, elevation_angle, RIS_list)
        
def angle_loop(freq_data : list, azimuth_steps_form_start : int, elevation_steps_from_start : int, elevation_no_angles : int) -> bool:
    for i in range(azimuth_no_angles+1):
        azimuth_angle = count_angle(azimuth_steps_form_start)
        print(f"######################[AZYMUT]: - {azimuth_angle} ############################")
        for i in range(elevation_no_angles+1):
            elevation_angle = count_angle(elevation_steps_from_start)
            freq_loop(freq_data, azimuth_angle, elevation_angle)
            print("[Aktualny kąt elewacji]: ", elevation_angle)
            print("[Ilość kroków od początku]: ", elevation_steps_from_start)
            remote_head.rotate_up(elevation_step)
            time.sleep(1.5) # wait for remote_head stabilization
            elevation_steps_from_start+=elevation_step
        time.sleep(1.5)
        remote_head.rotate_down((2*elevation_steps_from_start) - elevation_step) # back to elevation start postion
        time.sleep(1.5)
        elevation_steps_from_start = -elevation_start_position
        remote_head.rotate_right(azimuth_step) # movee few steps to the right (descroption in config file)
        azimuth_steps_form_start += azimuth_step
    return True

def ris_usb_init() -> list:
    RIS_list = []
    id = 0
    for port in ris_ports:
        RIS_list.append(RIS_usb(port, id))
        id+=1
    for ris in RIS_list:
        ris.reset()
        print(ris.port)
        print(ris.id)
    return RIS_list   
   
    
if __name__=="__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        remote_head.resolution(step_resolution)
        remote_head.rotate_down(elevation_start_position)
        elevation_steps_from_start = -elevation_start_position
        azimuth_steps_from_start = 0 # counts how many steps remote head did. Could be used to count actual measurement angle.
        RIS_list = ris_usb_init()
        freq_data = prepare_freq()
        measure_ended = angle_loop(freq_data, azimuth_steps_from_start, RIS_list)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()

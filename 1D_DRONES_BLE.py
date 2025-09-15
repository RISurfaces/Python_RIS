from bleak import *
import asyncio
import time
import json
import analyzer
import generator
import numpy as np
from RsSmw import *

try:
    with open("config.json") as config_f:
        config = json.load(config_f)
        RIS_SET_TIME_BLE = config["RIS_SET_TIME_BLE"]
        WRITE_UUID = config["WRITE_UUID"]
        READ_UUID = config["READ_UUID"]
        DESCRIPTOR_NUMBER = config["DESCRIPTOR_NUMBER"]
        trace_file = config["TRACE_FILE"]
        start_freq = config["START_FREQ"]
        end_freq = config["END_FREQ"]
        step_freq = config["STEP_FREQ"]
        span = config["SPAN"]
        analyzer_mode = config["ANALYZER_MODE"]
        revlevel = config["REVLEVEL"]
        rbw = config["RBW"]
        generator_amplitude = config["GENERATOR_AMPLITUDE"]
        pattern_for_negation = config["ID_FOR_NEGATION"]
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else:
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()
    
try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()

class RIS_ble:
    def __init__(self, ble_name: str, id: int) -> None:
        self.ble_name = ble_name
        self.id = id

    async def _set_multiple_patterns(self, patterns: json) -> str:
        # /---------------SKRYPT DO POMIARU DRONY-----------------/
        generator.meas_prep(True, generator_mode, generator_amplitude, start_freq)
        for pattern in patterns:
            command_data = (
                bytearray([0x01])
                + f"!{pattern["HEX"]}".encode("utf-8")
                + bytearray([0x0A])
            )
            try:
                await self.client.write_gatt_char(WRITE_UUID, command_data, False)
            except BleakCharacteristicNotFoundError:
                print(
                    "[BLE_ERROR] There is no such write charactristic. Check config file."
                )
                exit()
            try:
                response = await self.client.read_gatt_char(READ_UUID)
            except BleakCharacteristicNotFoundError:
                print(
                    "[BLE_ERROR] There is no such read charactristic. Check config file."
                )
                exit()
            analyzer.meas_prep(start_freq, span, analyzer_mode, revlevel, rbw)
            with open(trace_file, "a+") as file:
                file.write(pattern["ID"] + ";")
                file.close()  # CLose the file
                analyzer.trace_get(trace_file)
        return response

    async def connect_multiple_patterns(self, patterns: json) -> str:
        try:
            devices = await BleakScanner.discover()
            self.device = next((d for d in devices if d.name == self.ble_name), None)
            if not self.device:
                raise BleakError
            print(
                f"[BLE INFO] Device {self.ble_name} with addres {self.device.address} was found. ID of the device is {self.id}."
            )
        except BleakError:
            print("[BLE ERROR] Device with given name was not found.")
            return False
        async with BleakClient(self.device) as self.client:
            print(f"[BLE INFO] Connected to device {self.ble_name}.")
            try:
                await self.client.write_gatt_descriptor(DESCRIPTOR_NUMBER, b"\x01\x00")
            except BleakError:
                print(
                    f"[BLE_ERROR] There is no such descriptor. Change value in config to 16."
                )
                return False
            await asyncio.sleep(0.1)
            response = await self._set_multiple_patterns(patterns)
            return response


input("Potwierdz start pomiaru: ")
ris_ble = RIS_ble("A-3163CA", 0)
response = asyncio.run(ris_ble.connect_multiple_patterns(patterns_data))
print(response)
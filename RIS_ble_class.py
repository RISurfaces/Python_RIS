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
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()


class RIS_ble:
    def __init__(self, ble_name: str, id: int) -> None:
        self.ble_name = ble_name
        self.id = id

    async def _set_pattern(self, pattern: str) -> str:
        command_data = (
            bytearray([0x01]) + f"!0x{pattern}".encode("utf-8") + bytearray([0x0A])
        )
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        time.sleep(RIS_SET_TIME_BLE)
        try:
            response = await self.client.read_gatt_char(READ_UUID)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        return response

    async def _set_multiple_patterns(self, patterns: json) -> str:
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
            time.sleep(RIS_SET_TIME_BLE)
            # tu kod do obslugi pomiaru w tej wersji
            try:
                response = await self.client.read_gatt_char(READ_UUID)
            except BleakCharacteristicNotFoundError:
                print(
                    "[BLE_ERROR] There is no such read charactristic. Check config file."
                )
        return response

    async def _reset(self) -> bool:
        command_data = bytearray([0x01]) + "!Reset".encode("utf-8") + bytearray([0x0A])
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        await asyncio.sleep(0.1)
        return True

    async def _read_EXT_voltage(self) -> str:
        command_data = bytearray([0x01]) + f"?Vext".encode("utf-8") + bytearray([0x0A])
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        await asyncio.sleep(0.2)
        try:
            response = await self.client.read_gatt_char(READ_UUID)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        return response

    async def _read_pattern(self) -> str:
        command_data = (
            bytearray([0x01]) + f"?Pattern".encode("utf-8") + bytearray([0x0A])
        )
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        await asyncio.sleep(0.1)
        try:
            response = await self.client.read_gatt_char(READ_UUID)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        return response

    async def connect(self) -> bool:
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
            return True

    async def connect_reset(self) -> bool:
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
            response = await self._reset()
            return response

    async def connect_pattern(self, pattern: str) -> str:
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
            response = await self._set_pattern(pattern)
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

    async def connect_read_voltage(self) -> str:
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
            response = await self._read_EXT_voltage()
            return response

    async def connect_read_pattern(self) -> bool:
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
            response = await self._read_pattern()
            return response

    def ris_pattern_negation(self, pattern: str) -> str:
        pattern = int(pattern, 16)
        pattern = (
            ~pattern
            & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        )
        pattern = hex(pattern)
        pattern = str(pattern)
        no_of_zero_to_add = 66 - len(pattern)
        for i in range(no_of_zero_to_add):
            pattern = pattern[:2] + "0" + pattern[2:]
        pattern = pattern.upper()
        pattern = pattern.replace("X", "x")
        return pattern

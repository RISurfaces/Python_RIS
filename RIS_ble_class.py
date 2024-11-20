from bleak import *
import asyncio
import time
import json


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
                self.device = next(
                    (d for d in devices if d.name == self.ble_name), None
                )
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
                    await self.client.write_gatt_descriptor(
                        DESCRIPTOR_NUMBER, b"\x01\x00"
                    )
                except BleakError:
                    print(
                        f"[BLE_ERROR] There is no such descriptor. Change value in config to 16."
                    )
                    return False
                await self.reset()
                return True

    async def reset(self) -> str:
        command_data = bytearray([0x01]) + "!Reset".encode("utf-8") + bytearray([0x0A])
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        time.sleep(RIS_SET_TIME_BLE)

    async def connect_pattern(self, pattern: str) -> bool:
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
            await self.set_pattern(pattern)
            return True

    async def set_pattern(self, pattern: str) -> str:
        command_data = (
            bytearray([0x01]) + f"{pattern}".encode("utf-8") + bytearray([0x0A])
        )
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        time.sleep(RIS_SET_TIME_BLE)
        try:
            response = await self.client.read_gatt_char(READ_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        print(response)
        return response

    async def set_pattern(self, pattern: str) -> str:
        command_data = bytearray([0x01]) + f"?Vext".encode("utf-8") + bytearray([0x0A])
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        time.sleep(RIS_SET_TIME_BLE)
        try:
            response = await self.client.read_gatt_char(READ_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        print(response)
        return response

    async def set_pattern(self, pattern: str) -> str:
        command_data = (
            bytearray([0x01]) + f"?Pattern".encode("utf-8") + bytearray([0x0A])
        )
        try:
            await self.client.write_gatt_char(WRITE_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print(
                "[BLE_ERROR] There is no such write charactristic. Check config file."
            )
        time.sleep(RIS_SET_TIME_BLE)
        try:
            response = await self.client.read_gatt_char(READ_UUID, command_data, False)
        except BleakCharacteristicNotFoundError:
            print("[BLE_ERROR] There is no such read charactristic. Check config file.")
        print(response)
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

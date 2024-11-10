import asyncio
#import RIS_usb_class
from bleak import *

#set key
#ris = RIS_usb_class.RIS_usb('COM7', 1)
#ris.read_EXT_voltage()
#ris.set_BT_key(12345)

#find devices
import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)
    ble_address = "6C:3E:67:FC:CD:06"
    async with BleakClient(ble_address) as client:
        # we’ll do the read/write operations here
        print("Connected to BLE device")
        print(client.is_connected)   

asyncio.run(main())

#check characteristic

#ris = RIS_usb_class.RIS_usb('COM7', 1)
#ris.set_BT_key('12345')

    
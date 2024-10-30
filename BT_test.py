import asyncio
import RIS_usb_class
from bleak import *

#set key
ris = RIS_usb_class.RIS_usb('COM7', 1)
ris.read_EXT_voltage()
ris.set_BT_key(12345)

#find devices
async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
loop = asyncio.get_event_loop()
loop.run_until_complete(run())

#check characteristic
MAC = '00:18:DA:31:63:CB'
ris = RIS_usb_class.RIS_usb('COM7', 1)
ris.set_BT_key('12345')
async def connection():
    client = BleakClient(MAC)
    await client.connect()
    My_services = await client.get_services()
    for s in My_services:
        print(s) # will print all the servies the device is sending
        My_chars =  s.get_characteristic(s)
        print(str(My_chars))
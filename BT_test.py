import asyncio
from bleak import *


WRITE = "6e400002-c352-11e5-953d-0002a5d5c51b"
READ = "6e400003-c352-11e5-953d-0002a5d5c51b"
async def main():
    devices = await BleakScanner.discover()
    #for device in devices:
        #print(device)
    ble_address = "00:18:DA:32:38:8F"
    async with BleakClient(ble_address) as client:
        # we’ll do the read/write operations here
        print("Connected to BLE device")
        print(client.is_connected)
        await client.write_gatt_char(WRITE,b"?SerialNo", response=True)
        await asyncio.sleep(0.5)
        response = await client.read_gatt_char(READ)
        print(response)

asyncio.run(main())

    
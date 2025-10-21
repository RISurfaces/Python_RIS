from RIS_ble_class import RIS_ble
import asyncio
ris_ble = RIS_ble("A-32388D", 0)
connect = asyncio.run(ris_ble.connect_reset())

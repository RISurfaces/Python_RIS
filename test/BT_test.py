import asyncio
from bleak import BleakScanner, BleakClient

# Zdefiniowane identyfikatory UUID dla charakterystyk
WRITE = ["6e400002-c352-11e5-953d-0002a5d5c51b"]

READ = [
    "6e400003-c352-11e5-953d-0002a5d5c51b",
]

PATTERN = "!0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"


async def main():
    # Wyszukiwanie urządzeń BLE
    devices = await BleakScanner.discover()
    if not devices:
        print("Nie znaleziono żadnych urządzeń BLE!")
        return

    # Wybierz urządzenie po jego adresie (jeśli jest znany) lub po nazwie
    ble_address = [
        "00:18:DA:32:38:8F",  # A32388F
        "00:18:DA:32:38:8D",  # A32388D
    ]  # adres MAC Twojego urządzenia BLE
    for adress in ble_address:
        device = next((d for d in devices if d.address == adress), None)
        if not device:
            print(f"Nie znaleziono urządzenia z adresem {adress}")
            continue
        print(f"Znaleziono urządzenie: {device.name} ({device.address})")

        # Łączenie się z urządzeniem BLE
        async with BleakClient(device) as client:
            print(f"Połączono z urządzeniem: {device.name}")

            # Przykładowe zapisanie danych w descriptorze (upewnij się, że używasz odpowiedniego UUID)
            try:
                await client.write_gatt_descriptor(16, b"\x01\x00")
            except Exception as e:
                print(f"Błąd podczas zapisywania descriptora: {e}")

            print(f"Połączono: {client.is_connected}")

            # Pisanie do charakterystyk (WRITE)
            for characteristic in WRITE:
                try:
                    print(f"Pisanie do charakterystyki: {characteristic}")
                    command_data = (
                        bytearray([0x01]) + PATTERN.encode("utf-8") + bytearray([0x0A])
                    )
                    await client.write_gatt_char(
                        characteristic, command_data, response=False
                    )
                except Exception as e:
                    print(f"Błąd podczas pisania do {characteristic}: {e}")

            await asyncio.sleep(0.1)

            # Odczyt danych z charakterystyk (READ)
            for characteristic in READ:
                try:
                    print(f"Odczyt z charakterystyki: {characteristic}")
                    response = await client.read_gatt_char(characteristic)
                    print(f"Odpowiedź z {characteristic}: {response}")
                except Exception as e:
                    print(f"Błąd podczas odczytu z {characteristic}: {e}")


# Uruchomienie aplikacji
asyncio.run(main())

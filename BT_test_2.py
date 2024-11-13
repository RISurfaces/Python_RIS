from bleak import BleakClient
import asyncio


class RIS_BTLE_Interface:
    def __init__(self, bt_name):
        self.bt_name = bt_name
        self.client = None
        self.write_characteristic_uuid = (
            "6E400002-C352-11E5-953D-0002A5D5C51B"  # UUID dla zapisu
        )
        self.read_characteristic_uuid = (
            "6E400003-C352-11E5-953D-0002A5D5C51B"  # UUID dla odczytu
        )

    async def init(self):
        self.client = BleakClient(self.bt_name)
        await self.client.connect()

        if self.client.is_connected:
            print("Połączono z urządzeniem BLE.")
            # Subskrybuj charakterystykę do odczytu
            await self.client.start_notify(
                self.read_characteristic_uuid, self.notification_handler
            )
        else:
            print("Nie udało się połączyć z urządzeniem.")

    async def notification_handler(self, sender, data):
        # Funkcja obsługująca dane przychodzące przez notyfikacje
        print(f"Otrzymano dane od {sender}: {data}")

    async def send_command(self, command):
        # Konwertuj polecenie do formatu odpowiedniego dla BLE
        # Rozbij `command` na bajty jeśli potrzeba, np. jeśli `command` to liczba 32-bitowa
        start_byte = 0x01
        end_byte = 0x0A

        # W razie potrzeby konwertuj `command` do odpowiednich bajtów
        if isinstance(command, int):
            # Konwertuj 32-bitową liczbę na 4 bajty
            command_bytes = command.to_bytes(4, byteorder="big")
        elif isinstance(command, str):
            command_bytes = command.encode("utf-8")  # Konwertuj string na bajty
        else:
            raise ValueError("Nieznany typ dla `command`.")

        data = bytearray([start_byte]) + command_bytes + bytearray([end_byte])

        # Wyślij dane do urządzenia
        await self.client.write_gatt_char(self.write_characteristic_uuid, data)

    async def read_serial_number(self):
        # Wyślij komendę i odczytaj odpowiedź
        await self.send_command("?SerialNo")
        # Odczytanie może wymagać obsługi odpowiedzi przez callback lub bezpośredniego odczytu,
        # w zależności od urządzenia i usługi

    async def deinit(self):
        # Odłącz klienta BLE
        if self.client:
            await self.client.disconnect()
            print("Odłączono od urządzenia BLE.")


# Przykład użycia
async def main():
    bt_device_name = "Nazwa_Urządzenia_BLE"
    ris_interface = RIS_BTLE_Interface(bt_device_name)

    await ris_interface.init()
    await ris_interface.send_command(0xFFFFFFFF)  # Przykład: wysłanie 32-bitowej liczby
    await ris_interface.deinit()


# Uruchomienie głównej funkcji
asyncio.run(main())

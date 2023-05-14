import asyncio
from bleak import BleakClient, BleakScanner
DEVICE_ADDR = ""

async def main():
    devices = await BleakScanner.discover()
    for i, d in enumerate(devices):
        print(f"[{i}] {d}")
    # choice = int(input("> "))
    async with BleakClient(DEVICE_ADDR) as client:
        for service in client.services:
            print(f"SERVICE: HANDLE={service.handle} UUID={service.uuid} DESCRIPTION={service.description}")
            for char in service.characteristics:
                print(f"    \-> CHARACTERISTIC - HANDLE={char.handle} UUID={char.uuid} DESCRIPTION={char.description} PROPERTIES={char.properties}")
                for desc in char.descriptors:
                    print(f"        \-> DESCRIPTOR - {desc}")
        CONTROL_CHAR = ""
        await client.write_gatt_char(
                    CONTROL_CHAR,
                    data=bytes.fromhex("242a2b42")
                )
        while True:
            command = input("> ")
            if command == "on":
                await client.write_gatt_char(
                    CONTROL_CHAR,
                    data=bytes.fromhex("cc2333")
                )
            elif command == "off":
                await client.write_gatt_char(
                    CONTROL_CHAR,
                    data=bytes.fromhex("cc2433")
                )
            else:
                if len(command) == 6:
                    color = f"56{command}00f0aa"
                    await client.write_gatt_char(
                        CONTROL_CHAR,
                        data=bytes.fromhex(color)
                    )
                else:
                    print("[!] Hex color must be triplet")
asyncio.run(main())
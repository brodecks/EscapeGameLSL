import asyncio
from bleak import BleakScanner, BleakClient
from pylsl import StreamInfo, StreamOutlet

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


async def run():
    #creation flux
    info = StreamInfo('PolarH10', 'HR', 1, 1, 'float32', 'mint_polar_001')
    outlet = StreamOutlet(info)

    print("Recherche de la ceinture Polar H10...")
    # On cherche les appareils Bluetooth autour
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and "Polar H10" in d.name
    )

    if not device:
        print("Ceinture non trouvée. Vérifiez qu'elle est portée et non connectée au téléphone.")
        return

    def callback(sender, data):
        # data[1] contient les BPM (Fréquence Cardiaque)
        hr_bpm = data[1]
        print(f"BPM envoyé vers LSL: {hr_bpm}")
        outlet.push_sample([float(hr_bpm)])

    async with BleakClient(device) as client:
        print(f"Connecté à {device.name} [{device.address}]")
        # On s'abonne aux notifications de fréquence cardiaque
        await client.start_notify(HR_UUID, callback)

        # Le script tourne tant qu'on ne l'arrête pas (Ctrl+C)
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Arrêt du flux.")

from winrt.windows.devices.radios import Radio, RadioKind
import concurrent.futures

def get_radios():
    return Radio.get_radios_async().get()

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    radios = executor.submit(get_radios).result()

bluetooth = next(r for r in radios if r.kind == RadioKind.BLUETOOTH)

print("Bluetooth state:", bluetooth.state)

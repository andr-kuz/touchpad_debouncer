import asyncio
from evdev import InputDevice, list_devices, ecodes

async def monitor_keyboard():
    devices = [InputDevice(path) for path in list_devices()]
    keyboard_devices = [dev for dev in devices if ecodes.EV_KEY in dev.capabilities()]
    
    for device in keyboard_devices:
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                print("Key event detected")
                # Your logic here

asyncio.run(monitor_keyboard())

# utils.py
from typing import Optional
import asyncio
from evdev import InputDevice, list_devices, ecodes
from device_controller import controller

class ReusableTimer:
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.timer_handle = None
        self._create_new_timer()

    def _create_new_timer(self):
        loop = asyncio.get_event_loop()
        self.timer_handle = loop.call_later(self.interval, self.function)

    def reset(self):
        if self.timer_handle:
            self.timer_handle.cancel()
        self._create_new_timer()

timer = ReusableTimer(0.2, controller.enable_device)

async def handle_key_event():
    controller.disable_device()
    timer.reset()

def get_main_keyboard() -> Optional[InputDevice]:
    keyboard_priority = [
        'keyd virtual keyboard',         # keyd virtual device
        'AT Translated Set 2 keyboard',  # Standard physical keyboard (most Linux)
        'Virtual core keyboard',         # Xorg virtual keyboard
        'Apple Internal Keyboard',       # Mac keyboards
        'Microsoft Surface Keyboard',    # Surface devices
        'Logitech Keyboard',             # Common external keyboard
    ]
    
    devices = [InputDevice(path) for path in list_devices()]
    keyboards = [dev for dev in devices if ecodes.EV_KEY in dev.capabilities()]
    
    # Try priority devices first
    for name in keyboard_priority:
        for dev in keyboards:
            if dev.name == name:
                return dev
    
    # Fallback to first keyboard with many keys (likely main keyboard)
    if keyboards:
        return max(keyboards, key=lambda d: len(d.capabilities().get(ecodes.EV_KEY, [])))
    
    return None

async def monitor_device(name: Optional[str] = None) -> None:
    while True:
        try:
            if not name:
                device = get_main_keyboard()
            else:
                devices = [InputDevice(path) for path in list_devices()]
                device = next(
                    (dev for dev in devices 
                     if dev.name == name),
                    None
                )

            if not device:
                print(f'{name} device not found')
                continue

            print(f'Monitoring device at {device.path}')

            async for event in device.async_read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    await handle_key_event()
        except Exception as e:
            print(f'Unexpected error: {e}')
        print('sleeping')
        await asyncio.sleep(3)

def run_event_loop():
    asyncio.run(monitor_device())

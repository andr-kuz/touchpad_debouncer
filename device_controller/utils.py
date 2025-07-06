from evdev import InputDevice, list_devices, ecodes
from typing import Optional
import os
import glob

def get_event_device_by_pattern(name_pattern: str) -> Optional[str]:
    for name in glob.glob('/sys/class/input/event*/device/name'):
        try:
            with open(name, 'r') as f:
                if name_pattern in f.read():
                    device = name.replace('/device/name', '')
                    return f'/dev/input/{os.path.basename(device)}'
        except IOError:
            continue
    return None

def debug_devices():
    for path in list_devices():
        try:
            dev = InputDevice(path)
            print(f"\nDevice: {dev.path} ({dev.name})")
            print("Capabilities:")
            if ecodes.EV_KEY in dev.capabilities():
                print("  Keyboard device")
                print(f"  Supported keys: {dev.capabilities()[ecodes.EV_KEY]}")
            else:
                print("  Not a keyboard device")
        except Exception as e:
            print(f"Error checking {path}: {e}")


if __name__ == '__main__':
    debug_devices()
    # print(get_event_device_by_pattern('keyd virtual pointer'))
    # exit(1)

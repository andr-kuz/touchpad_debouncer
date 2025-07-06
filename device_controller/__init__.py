from .device_controller import DeviceController
from .utils import get_event_device_by_pattern



device_path = get_event_device_by_pattern('ASCP1A00:00 093A:3013 Touchpad')
if not device_path:
    raise Exception('Device not found')

controller = DeviceController(device_name=device_path)

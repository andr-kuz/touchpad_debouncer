# device_controller.device_controller.py
from dataclasses import dataclass
import subprocess
import logging


@dataclass
class DeviceController:
    device_name: str
    lock_process_pid: int = 0

    def disable_device(self) -> None:
        if self.lock_process_pid == 0:
            print('disable')
            proc = subprocess.Popen(['evtest', '--grab', self.device_name],
                                  stdout=subprocess.DEVNULL)
            self.lock_process_pid = proc.pid

    def enable_device(self) -> None:
        if self.lock_process_pid > 0:
            print('enable')
            subprocess.run(['kill', str(self.lock_process_pid)], check=False)
            self.lock_process_pid = 0

    def __del__(self):
        try:
            self.enable_device()
        except Exception as e:
            logging.warning(f"Failed to enable device during destruction: {e}")

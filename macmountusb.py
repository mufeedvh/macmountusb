import subprocess
import time
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Static
from textual.containers import Container
from textual.timer import Timer

class USBDevice:
    def __init__(self, product_id, vendor_id, serial_number, speed, manufacturer, location_id, bsd_name, capacity, file_system, volume_name):
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.serial_number = serial_number
        self.speed = speed
        self.manufacturer = manufacturer
        self.location_id = location_id
        self.bsd_name = bsd_name
        self.capacity = capacity
        self.file_system = file_system
        self.volume_name = volume_name

    def __str__(self):
        return f"{self.manufacturer} {self.volume_name} ({self.capacity}) - {self.bsd_name}"

def get_usb_devices():
    output = subprocess.check_output(['system_profiler', 'SPUSBDataType']).decode()
    devices = {}
    lines = output.splitlines()

    current_device = {}
    device_id = 0
    
    volume_name_line = False

    for line in lines:
        line = line.strip()

        if line.startswith('Product ID:'):
            device_id += 1
            current_device = {}

        if line.startswith('Product ID:'):
            current_device['product_id'] = line.split(': ')[1]
        elif line.startswith('Vendor ID:'):
            current_device['vendor_id'] = line.split(': ')[1].split(' ')[0]
        elif line.startswith('Serial Number:'):
            current_device['serial_number'] = line.split(': ')[1]
        elif line.startswith('Speed:'):
            current_device['speed'] = line.split(': ')[1]
        elif line.startswith('Manufacturer:'):
            current_device['manufacturer'] = line.split(': ')[1]
        elif line.startswith('Location ID:'):
            current_device['location_id'] = line.split(': ')[1]
        elif line.startswith('BSD Name:'):
            current_device['bsd_name'] = line.split(': ')[1]
        elif line.startswith('Capacity:'):
            current_device['capacity'] = line.split(': ')[1]
        elif line.startswith('File System:'):
            current_device['file_system'] = line.split(': ')[1]
        elif line.startswith('Media:'):
            volume_name_line = True
            continue

        if volume_name_line:
            current_device['volume_name'] = line.split(':')[0].strip()
            volume_name_line = False

        if 'bsd_name' in current_device and current_device['bsd_name'].startswith('disk') and len(current_device) == 10:
            devices[device_id] = USBDevice(**current_device)
            current_device = {}

    sorted_devices = dict(sorted(devices.items()))
    
    for k, v in sorted_devices.items():
        print(k, v)

    return sorted_devices

class MacMountUSB(App):
    CSS = """
    Screen {
        align: center middle;
        background: #282c34;
    }
    ListView {
        border: wide green;
        width: 80%;
        height: 60%;
    }
    ListItem {
        padding: 1;
        border-bottom: solid green;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(id="device_list")
        yield Footer()

    def on_mount(self) -> None:
        self.update_device_list()

    def update_device_list(self) -> None:
        device_list = self.query_one("#device_list", ListView)
        device_list.clear()
        self.devices = get_usb_devices()

        for device in self.devices.values():
            item = ListItem(Static(device.__str__()), id=device.bsd_name)
            device_list.append(item)

    async def on_list_view_selected(self, message: ListView.Selected) -> None:
        bsd_name = message.item.id
        device = next(d for d in self.devices.values() if d.bsd_name == bsd_name)
        self.mount_device(device)

    def mount_device(self, device: USBDevice) -> None:
        subprocess.run(['sudo', 'hdiutil', 'attach', '-nomount', f'/dev/{device.bsd_name}'])
        self.show_success_message(f"Mounted {device.manufacturer} {device.volume_name}")

    def show_success_message(self, message: str) -> None:
        container = Container(
            Static(message, id="success_message"),
            id="message_container"
        )
        self.mount(container)
        self.exit()

if __name__ == "__main__":
    USBMountApp().run()

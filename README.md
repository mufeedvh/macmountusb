# MacMountUSB

MacMountUSB is a Textual-based TUI (Text User Interface) application for macOS that helps you list and mount USB devices using a user-friendly interface. The application parses the output from `system_profiler` and allows you to mount selected USB devices using `hdiutil`.

# For?

- MacOS failing to mount your external drives? Use this tool.
- MacOS Disk Utility stuck on loading? Use this tool.
- Manually mounting the USB device with diskutil isn't working? Use this tool.
- You have a SanDisk Extreme Portable SSD and MacOS can't detect it? ...Yeah, use this tool.

## Requirements

- macOS
- Python 3.7+
- Textual library

## Installation

1. Clone the repository:

```sh
git clone https://github.com/mufeedvh/macmountusb.git
cd macmountusb
```

2. Create a virtual environment (optional but recommended):

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required dependencies:

```sh
pip install textual
```

## Usage

1. Run the application:

```sh
sudo python3 macmountusb.py
```

2. Use the arrow keys to navigate through the list of USB devices.
3. Press Enter to select a device and mount it.

## License

This project is licensed under the MIT License.

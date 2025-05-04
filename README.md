# OS Flip 🌀

*A simple script to switch your default OS at boot time*

## Overview

**OS Flip** is a Python script that lets you view, select, and switch the default boot OS using GRUB on dual-boot Linux systems. Whether you're temporarily booting into another OS or setting a new default, this script makes it easy from the terminal.

## Features

* 🔍 Lists all available GRUB boot entries
* ✅ Set a default OS for future boots
* 🚀 Option to just reboot into another OS once
* 🛡️ Root check to avoid permission errors
* 🧠 Auto-detects GRUB update command based on your Linux distro

## Requirements

* Python 3
* A Linux system using GRUB
* Root privileges (`sudo`)

## Usage

```bash
sudo python3 OS\ Flip.py
```

### Menu Options

1. **Set default boot OS**
   Permanently changes the GRUB default to the selected OS.

2. **Just boot into another**
   Temporarily boots into a different OS on the next reboot.

3. **Exit**
   Quits the script.

## Example Output

```
=== Available Boot Entries ===
1. Ubuntu
2. Windows Boot Manager (on /dev/sda1)

Options:
1. Set default boot OS
2. Just boot into another
3. Exit
```

## Notes

* This script modifies `/etc/default/grub` and runs `update-grub` or `grub2-mkconfig`, depending on your distro.
* Make sure GRUB is configured correctly and backed up if needed before changing defaults.

## Tested On

* Debian-based systems (Ubuntu, Pop!\_OS)
* Red Hat-based systems (Fedora)

## Disclaimer

Use at your own risk. While the script is designed to be safe, messing with bootloaders can be risky if done carelessly.

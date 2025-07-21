# OS Flip 🌀

*A cross-platform terminal tool to view, set, and flip your default boot OS on Linux, Windows, and macOS.*

---

## ✨ Overview

**OS Flip** is a Python-based utility to manage boot preferences across dual-boot or multi-boot systems. Whether you're switching between Linux and Windows or managing a macOS Boot Camp setup, OS Flip gives you a simple terminal UI to:

- 🔍 View bootable OS entries
- ✅ Set the **default OS**
- 🔁 Temporarily Flips into another OS

---

## 🖥️ Platforms Supported

- 🐧 **Linux** (GRUB2)
- 🪟 **Windows** (`bcdedit`)
- 🍎 **macOS** (`bless`) — *experimental*

---

## ⚙️ Features

- 🧠 Auto-detects current OS
- 📜 Lists all boot entries
- ✅ Set permanent default boot entry
- 🔁 Flip OS temporarily
- 💬 Color-coded terminal UI
- 📁 Logs activity to a platform-specific log file
- 🪟 [Windows `.exe` version available](https://github.com/AKris15/OS-Flip/releases/latest)

---

## 📦 Installation

### ✅ Via pip (All Platforms)

```bash
pip install os-flip
````

Then run:

```bash
sudo os-flip  # On Linux/macOS
os-flip       # On Windows (admin)
```

> Requires Python 3.6+

### 📥 Windows `.exe` (no Python required)

[➡️ Download from GitHub Releases](https://github.com/AKris15/OS-Flip/releases/latest/download/Os-Flip.exe)

> Right-click → Run as Administrator
> May trigger SmartScreen warning (unsigned binary)

---

## 📋 Requirements

### Linux:

* Python 3
* GRUB2 bootloader
* `os-prober`, `update-grub` or `grub2-mkconfig`
* `sudo` or root privileges

### Windows:

* Python 3 (for pip version)
* Admin privileges
* `bcdedit` access

### macOS:

* Python 3
* Tools: `diskutil`, `systemsetup`, `bless`
* Run with `sudo`
* ⚠️ SIP and volume restrictions may apply

---

## 🚀 Example Output

```text
   ____   _____          ______ _      _____ _____ 
  / __ \ / ____|        |  ____| |    |_   _|  __ \
 | |  | | (___    ___   | |__  | |      | | | |__) |
 | |  | |\___ \         |  __| | |      | | |  ___/ 
 | |__| |____) |        | |    | |____ _| |_| |     
  \____/|_____/         |_|    |______|_____|_|   

         Welcome to OS FLIP 
                         By - AK (Your OS)

📜 Available Boot Entries:
  1. Windows Boot Manager (on /dev/nvme0n1p1) (Current Default)
  2. Fedora Linux

⚙️  Options:
  1. Set default boot OS
  2. Flip OS
  3. Exit
```

---

## 📂 Log Location

| OS      | Log File Path                   |
| ------- | ------------------------------- |
| Linux   | `/tmp/os_flip_<username>.log`   |
| macOS   | `/tmp/os_flip_<username>.log`   |
| Windows | `%TEMP%\os_flip_<username>.log` |

---

## 🧪 Tested On

| OS            | Status          |
| ------------- | --------------- |
| Ubuntu 22.04  | ✅ Confirmed     |
| Fedora 40     | ✅ Confirmed     |
| Windows 10/11 | ✅ Confirmed     |
| macOS (Intel) | ⚠️ Experimental |

---

## 🚧 Disclaimer

> ⚠️ Use at your own risk. Editing bootloader configs may prevent systems from booting. Always back up and know what you're changing.

---

## 👨‍💻 Author

Made with ❤️ by **[AK](https://github.com/AKris15)**
MIT Licensed — attribution appreciated!

---

## 🔗 Related Links

* 📦 [PyPI Package](https://pypi.org/project/os-flip)
* 🪟 [Windows `.exe` Download](https://github.com/AKris15/OS-Flip/releases/latest/download/Os-Flip.exe)
* 🐛 [Issue Tracker](https://github.com/AKris15/OS-Flip/issues)

````

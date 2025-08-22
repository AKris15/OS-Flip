# OS-Flip 🌀

*A Linux terminal tool to view, set, and flip your default boot OS.*

---

## ✨ Overview

**OS Flip** is a Python-based utility to manage boot preferences on Linux systems using GRUB2. Whether you're running a dual-boot setup or switching between multiple Linux distributions, OS Flip gives you a simple terminal UI to:

* 🔍 View bootable OS entries
* ✅ Set the **default OS**
* 🔁 Temporarily flip into another OS for one-time boot

---

## 🖥️ Platforms Supported

* 🐧 **Linux only** (GRUB2-based bootloaders)

> Windows and macOS are **not supported**. Windows does not allow GRUB changes, and macOS/Boot Camp setups are incompatible. Any Linux distribution should manage BIOS/UEFI defaults through firmware settings.

---

## ⚙️ Features

* 🧠 Auto-detects current OS
* 📜 Lists all GRUB boot entries
* ✅ Set permanent default boot entry
* 🔁 Flip OS temporarily (one-time boot)
* 📁 Logs activity to a Linux-specific log file

---

## 📦 Installation

### **Requires root/sudo**

```bash
sudo pip install os-flip
```

Then run:

```bash
sudo os-flip
```

> Requires Python 3.6+

---

## 📋 Requirements

* Python 3
* GRUB2 bootloader
* `os-prober`, `update-grub` or `grub2-mkconfig`
* `sudo` or root privileges

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
  1. Fedora Linux (Current Default)
  2. Windows Boot Manager (on /dev/nvme0n1p1)

⚙️  Options:
  1. Set default boot OS
  2. Flip OS
  3. Exit
```

---

## 📝 Custom Shortcuts (Advanced)

### 1. Using a Text File

You can automate OS Flip actions using a simple **text file shortcut**.
For example, create a text file named `win_boot.txt` containing:

```
2
1
y
```

**Meaning:**

* `2` → Choose **Flip OS**
* `1` → Select OS option `1` (e.g., Windows Boot Manager) for **one-time boot**
* `y` → Confirm and reboot immediately

Run it with:

```bash
sudo os-flip < win_boot.txt
```

---

### 2. Create a Quick Command (Alias)

To make this even faster, add a shortcut to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
alias flip='sudo os-flip < /path/to/win_boot.txt'
```

After saving and reloading your shell (`source ~/.bashrc`), just type:

```bash
flip
```

…and your system will **instantly flip and reboot into the selected OS**.

---

## 📂 Log Location

| OS    | Log File Path                 |
| ----- | ----------------------------- |
| Linux | `/tmp/os_flip_<username>.log` |


## 🚧 Disclaimer

> ⚠️ Use at your own risk. Editing bootloader configs may prevent systems from booting. Always back up and know what you're changing.

---

## 👨‍💻 Author

Made with ❤️ by **[AK](https://github.com/AKris15)**
MIT Licensed — attribution appreciated!

---

## 🔗 Related Links

* 📦 [PyPI Package](https://pypi.org/project/os-flip)
* 🐛 [Issue Tracker](https://github.com/AKris15/OS-Flip/issues)

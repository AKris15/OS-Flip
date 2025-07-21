# OS Flip 🌀

*A multi-platform script to view and switch your default boot OS across Linux, Windows, and macOS.*

---

## ✨ Overview

**OS Flip** is a cross-platform Python utility to manage boot preferences on dual-boot or multi-boot systems. It allows you to:

- 🔍 View all bootable OS entries
- ✅ Set a default OS for future boots
- 🔁 Temporarily reboot into another OS (“Flip”)

It works on:

- 🐧 **Linux** (GRUB-based)
- 🪟 **Windows** (`bcdedit`)
- 🍎 **macOS** (`bless`) – ⚠️ *experimental and not fully tested*

Whether you're switching between Linux and Windows or managing a Boot Camp setup, **OS Flip** offers a simple, colorful terminal UI to handle it.

---

## ⚙️ Features

- 🧠 Auto-detects operating system
- 🔍 Lists all available boot entries
- ✅ Sets permanent default OS
- 🔁 Flips (reboots) temporarily into another OS
- 📁 Logs activity to platform-specific log file
- 💬 Color-coded terminal messages
- 🖥️ Launches in a new terminal window (if needed)

---

## 📦 Requirements

### 🐧 Linux:
- Python 3
- GRUB2 bootloader
- `update-grub` or `grub2-mkconfig`
- `os-prober`
- Run with `sudo` or as root

### 🪟 Windows:
- Python 3
- Run as Administrator
- `bcdedit` (pre-installed on Windows)

### 🍎 macOS (**experimental**):
- Python 3
- `diskutil`, `systemsetup`, `bless`
- Run with `sudo`

> ✅ Install Python dependency:
```bash
pip install colorama
````

---

## 🚀 Usage

Run the script with elevated privileges:

### On Linux/macOS:

```bash
sudo python3 os_flip.py
```

### On Windows:

Run Command Prompt or PowerShell **as Administrator**, then:

```cmd
python os_flip.py
```

---

## 🧪 Example Output

```
   ____   _____          ______ _      _____ _____ 
  / __ \ / ____|        |  ____| |    |_   _|  __ \
 | |  | | (___    ___   | |__  | |      | | | |__) |
 | |  | |\___ \         |  __| | |      | | |  ___/ 
 | |__| |____) |        | |    | |____ _| |_| |     
  \____/|_____/         |_|    |______|_____|_|   

         Welcome to OS FLIP 
                         By - AK (Linux)

ℹ️  Backed up GRUB config to /etc/default/grub.bak.1753056275  
✅ os-prober enabled.  
ℹ️  Updating GRUB entries... done

📜 Available Boot Entries:
  1. Windows Boot Manager (on /dev/nvme0n1p1) (Current Default)
  2. Fedora Linux

⚙️  Options:
  1. Set default boot OS
  2. Flip OS
  3. Exit
```

---

## 📂 Log Files

Activity is logged to a file based on your OS:

* **Linux/macOS:** `/tmp/os_flip_<username>.log`
* **Windows:** `%TEMP%\os_flip_<username>.log`

Useful for debugging or audit trails.

---

## 📌 Notes

* Linux: Edits `/etc/default/grub`, then runs `update-grub` or `grub2-mkconfig`
* macOS: Uses `bless` to set the startup disk (requires SIP-safe paths)
* Windows: Uses `bcdedit` to read/set boot configuration
* The script auto-launches in a new terminal if not already interactive
* GRUB backup is created before changes (`/etc/default/grub.bak.<timestamp>`)

---

## 🧪 Tested Platforms

| OS            | Status            |
| ------------- | ----------------- |
| Ubuntu        | ✅ Confirmed       |
| Fedora        | ✅ Confirmed       |
| Windows 10/11 | ✅ Confirmed       |
| macOS (Intel) | ⚠️ *Experimental* |

---

## 🛑 Disclaimer

> Use at your own risk. Modifying bootloader settings can affect system startup. Ensure you understand the implications, especially on production or encrypted systems.

---

## 👨‍💻 Author

**AK** – [github.com/AKris15](https://github.com/AKris15)

---

## 📜 License

MIT License

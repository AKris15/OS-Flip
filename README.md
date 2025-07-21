# OS Flip 🌀

*A multi-platform script to view and switch your default boot OS across Linux, Windows, and macOS.*

## ✨ Overview

**OS Flip** is a cross-platform Python script that helps you:

- View bootable OS entries
- Set the **default OS** for future boots
- Flip into another OS temporarily

It works on:
- ✅ Linux (GRUB-based bootloaders)
- ✅ Windows (via `bcdedit`)
- ⚠️ macOS (via `bless`, **not fully tested**)

Whether you dual-boot Linux and Windows or use macOS with Boot Camp, OS Flip gives you a simple terminal UI to control boot behavior.

---

## ⚙️ Features

- 🧠 Auto-detects OS and privileges
- 🔍 Lists available boot entries
- ✅ Set a default OS
- 🔁 Flips OS
- 💬 Color-coded terminal output
- 🧾 Logging to platform-specific log files
---

## 📦 Requirements

### 🐧 Linux:
- Python 3
- GRUB2 bootloader
- `update-grub` or `grub2-mkconfig`
- `os-prober`
- `sudo` or root access

### 🪟 Windows:
- Python 3
- Run as Administrator
- Access to `bcdedit` (built-in on Windows)

### 🍎 macOS (**not fully tested**):
- Python 3
- `diskutil`, `systemsetup`, `bless`
- Run with `sudo`

> ✅ `colorama` Python package is used for colored output. Install with:
```bash
pip install colorama

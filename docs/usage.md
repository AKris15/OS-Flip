# OS-Flip Usage Guide

A Python utility to manage boot preferences across Linux, Windows, and macOS.

---

## Installation
```bash
sudo pip install os-flip
```

Run with:
```bash
sudo os-flip [options]
```

> Requires Python 3.6+ and sudo/Administrator privileges

---

## Commands

### List Boot Entries
```bash
os-flip --list
os-flip -l
```

Example output:
```
  1. Arch Linux (Current Default)
  2. Windows Boot Manager
  3. Ubuntu 22.04
```

---

### Set Default OS
```bash
os-flip --set-default <INDEX>
os-flip -sd <INDEX>
```

Example:
```bash
sudo os-flip -sd 2
```

Prompts for immediate reboot after setting default.

---

### Flip OS (One-Time Boot)
```bash
os-flip --flip <INDEX>
os-flip -f <INDEX>
```

Example:
```bash
sudo os-flip -f 1
```

Boots into selected OS once, then returns to default.

---

### No Terminal Mode
```bash
os-flip --no-terminal [options]
os-flip -nt [options]
```

Example:
```bash
sudo os-flip -nt -l
```

---

### Clean Logs/Backups
```bash
os-flip --clean {l,b,lb}
os-flip -cl {l,b,lb}
```

Options: `l` (logs), `b` (backups), `lb` (both)

---

## Usage Examples

### Quick switch to Windows
```bash
sudo os-flip -l          # List entries
sudo os-flip -f 2        # Boot to entry #2
```

### Make Linux default
```bash
sudo os-flip -sd 1
```

### Create shell alias
Add to `~/.bashrc`:
```bash
alias flipwin='sudo os-flip -nt -f 2'
```

Use:
```bash
flipwin    # Instant reboot to Windows
```

---

## Requirements

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install os-prober grub2-common

# Arch
sudo pacman -S os-prober grub

# Fedora
sudo dnf install os-prober grub2-tools
```

**Windows:** BCDEdit (built-in)

**macOS:** diskutil/bless (built-in)

---

## Command Reference

| Command | Short | Description |
|---------|-------|-------------|
| `--list` | `-l` | List boot entries |
| `--set-default <INDEX>` | `-sd <INDEX>` | Set default OS |
| `--flip <INDEX>` | `-f <INDEX>` | One-time boot |
| `--no-terminal` | `-nt` | Run in current terminal |
| `--clean {l,b,lb}` | `-cl {l,b,lb}` | Clean logs/backups |
| `--help` | `-h` | Show help |

---

## Troubleshooting

**"Must be run as root"**
```bash
sudo os-flip -l
```

**"No boot entries found"**
```bash
sudo apt install os-prober  # Linux
```

**"grub-reboot not found"**
```bash
sudo apt install grub2-common  # Debian/Ubuntu
```

**Terminal issues**
```bash
sudo os-flip -nt -l  # Force current terminal
```

---

## Log Files

- Linux (root): `/var/log/os_flip.log`
- Linux/macOS (user): `/tmp/os_flip_<username>.log`
- Windows: `%TEMP%\os_flip_<username>.log`
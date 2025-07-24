#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path
import platform
import getpass
import time
from datetime import datetime
import plistlib
import shutil
import ctypes

# External
from colorama import init, Fore, Style

init(autoreset=True)

# --- Constants ---
LOG_FILE = (
    "/var/log/os_flip.log" if platform.system() == "Linux" 
    else os.path.join(os.environ['TEMP'], f"os_flip_{getpass.getuser()}.log") if platform.system() == "Windows"
    else f"/tmp/os_flip_{getpass.getuser()}.log"
)
USER_LOG_FILE = f"/tmp/os_flip_{getpass.getuser()}.log" if platform.system() in ("Linux", "Darwin") else None

# --- Logging ---
def log(message):
    path = LOG_FILE
    if platform.system() in ("Linux", "Darwin") and os.geteuid() != 0:
        path = USER_LOG_FILE
    
    try:
        with open(path, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except PermissionError:
        print(f"{Fore.RED}⚠️ Cannot write to log at {path}. Logging disabled.")

# --- Print Helpers ---
def print_success(msg): print(f"{Fore.GREEN}✅ {msg}"); log(f"SUCCESS: {msg}")
def print_info(msg): print(f"{Fore.CYAN}ℹ️  {msg}"); log(f"INFO: {msg}")
def print_warning(msg): print(f"{Fore.YELLOW}⚠️  {msg}"); log(f"WARNING: {msg}")
def print_error(msg): print(f"{Fore.RED}❌ {msg}"); log(f"ERROR: {msg}")

# --- Banner ---
def print_banner():
    if platform.system() == "Windows":
        color = Fore.BLUE
        os_name = "Windows"
    elif platform.system() == "Darwin":
        color = Fore.MAGENTA
        os_name = "macOS"
    else:  # Linux
        color = Fore.RED
        os_name = "Linux"
    
    banner = rf"""{color}{Style.BRIGHT}
   ____   _____          ______ _      _____ _____ 
  / __ \ / ____|        |  ____| |    |_   _|  __ \
 | |  | | (___    ___   | |__  | |      | | | |__) |
 | |  | |\___ \         |  __| | |      | | |  ___/ 
 | |__| |____) |        | |    | |____ _| |_| |     
  \____/|_____/         |_|    |______|_____|_|   
    
{Style.RESET_ALL}
{Style.BRIGHT}         Welcome to OS FLIP 
                            By - AK({os_name})
{Style.RESET_ALL}
"""
    print(banner)
    log(f"Launched OS Flip ({os_name})")

# --- Launches a New Terminal ---
def launch_in_new_terminal():
    """Try to launch the script in a new terminal window, or fallback to current."""
    current_os = platform.system()
    script_path = os.path.abspath(__file__)
    
    if current_os == "Windows":
        subprocess.Popen(f'start cmd /k python "{script_path}" --no-terminal-launch', shell=True)
        sys.exit(0)
    elif current_os == "Darwin":
        subprocess.Popen([
            "osascript",
            "-e", f'tell app "Terminal" to do script "python3 \'{script_path}\' --no-terminal-launch"'
        ])
        sys.exit(0)
    elif current_os == "Linux":
        terminals = [
            "gnome-terminal", "konsole", "xfce4-terminal", "xterm", "lxterminal",
            "tilix", "alacritty", "mate-terminal", "terminator", "urxvt", "st",
            "kitty", "deepin-terminal", "qterminal", "eterm", "mlterm", "wezterm", "foot"
        ]
        for term in terminals:
            if shutil.which(term):
                try:
                    subprocess.Popen([term, "-e", f"python3 '{script_path}' --no-terminal-launch"])
                    sys.exit(0)
                except Exception as e:
                    print_warning(f"Failed to launch with {term}: {e}")
        
        # Fallback prompt
        print_warning("⚠️ No supported terminal emulator found.")
        fallback = input("Would you like to run this script in the current terminal instead? (y/N): ").strip().lower()
        if fallback == "y":
            # Just continue running in this terminal (no recursion!)
            return
        else:
            print_error("Please install a terminal emulator (e.g., gnome-terminal or xterm).")
            sys.exit(1)

# --- Privilege Checks ---
def is_windows_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def exit_if_not_admin():
    if platform.system() == "Linux":
        if os.geteuid() != 0:
            print_error("This script must be run as root. Use `sudo`.")
            sys.exit(1)
    elif platform.system() == "Darwin":
        try:
            subprocess.run(["sudo", "-v"], check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print_error("This script must be run with sudo.")
            sys.exit(1)
    elif platform.system() == "Windows":
        if not is_windows_admin():
            print_error("This script must be run as Administrator.")
            sys.exit(1)

# --- Linux Specific Functions ---
def get_grub_update_cmd():
    if Path("/etc/debian_version").exists():
        return "update-grub"
    elif Path("/etc/redhat-release").exists() or "fedora" in platform.platform().lower():
        return "grub2-mkconfig -o /boot/grub2/grub.cfg"
    print_error("Unsupported Linux distribution.")
    sys.exit(1)

def update_grub():
    global GRUB_UPDATE_CMD
    try:
        subprocess.run(GRUB_UPDATE_CMD, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to update GRUB: {e}")
        return False

def backup_grub_config():
    timestamp = int(time.time())
    backup_path = f"/etc/default/grub.bak.{timestamp}"
    try:
        shutil.copy("/etc/default/grub", backup_path)
        print_info(f"Backed up GRUB config to {backup_path}")
        return True
    except Exception as e:
        print_error(f"Failed to backup GRUB config: {e}")
        return False

def ensure_os_prober_enabled():
    if not Path("/usr/bin/os-prober").exists():
        print_warning("os-prober not found. Some OSes may not be detected.")
        return False

    if not backup_grub_config():
        return False

    with open("/etc/default/grub", "r") as f:
        lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith("GRUB_DISABLE_OS_PROBER="):
            lines[i] = "GRUB_DISABLE_OS_PROBER=false\n"
            updated = True
            break

    if not updated:
        lines.append("GRUB_DISABLE_OS_PROBER=false\n")

    try:
        with open("/etc/default/grub", "w") as f:
            f.writelines(lines)
    except PermissionError as e:
        print_error(f"Failed to modify GRUB config: {e}")
        return False

    print_success("os-prober enabled.")
    print_info("Updating GRUB entries...")
    try:
        subprocess.run(["os-prober"], check=True)
        return update_grub()
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to run os-prober: {e}")
        return False
        
#Made By- https://github.com/AKris15

def get_linux_boot_entries():
    entries = []
    seen = set()

    grub_cfgs = [
        "/boot/grub/grub.cfg",
        "/boot/grub2/grub.cfg",
        "/boot/efi/EFI/fedora/grub.cfg"
    ]

    grub_path = next((p for p in grub_cfgs if Path(p).exists()), None)
    if grub_path:
        try:
            with open(grub_path, "r") as f:
                for line in f:
                    if line.strip().startswith("menuentry "):
                        # Extract exact title including quotes
                        title = line.split("'")[1]
                        if title not in seen:
                            entries.append(title)
                            seen.add(title)
        except Exception:
            pass
        
    bls_dir = Path("/boot/loader/entries")
    if bls_dir.exists():
        for entry in bls_dir.glob("*.conf"):
            with open(entry) as f:
                for line in f:
                    if line.startswith("title"):
                        title = line.strip().split(" ", 1)[1]
                        label = "Fedora Linux" if "Fedora" in title else title
                        if label not in seen:
                            entries.append(label)
                            seen.add(label)
                        break

    if not entries:
        print_error("No boot entries found.")
    return entries

def get_current_linux_default_os():
    try:
        with open("/etc/default/grub", "r") as f:
            for line in f:
                if line.startswith("GRUB_DEFAULT="):
                    return line.split("=", 1)[1].strip().strip('"')
    except:
        return None

def set_linux_default_os(entry_name):
    with open("/etc/default/grub", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("GRUB_DEFAULT="):
            lines[i] = f'GRUB_DEFAULT="{entry_name}"\n'
            break
    else:
        lines.append(f'GRUB_DEFAULT="{entry_name}"\n')

    with open("/etc/default/grub", "w") as f:
        f.writelines(lines)

    return update_grub()

# --- Windows Specific Functions ---
def get_windows_boot_entries():
    entries = []
    identifiers = []
    
    try:
        commands = [
            ["bcdedit", "/enum", "Firmware"],
            ["bcdedit", "/enum", "OSLOADER"],
            ["bcdedit"]  # Fallback
        ]
        
        for cmd in commands:
            if entries:  # Skip fallback if we already have entries
                break
                
            try:
                output = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
                
                current_identifier = None
                current_description = None
                
                for line in output.splitlines():
                    line = line.strip()
                    if line.startswith("identifier"):
                        current_identifier = line.split()[-1]
                    elif line.startswith("description"):
                        current_description = " ".join(line.split()[1:])
                        if current_identifier and current_description:
                            if current_description not in entries:  # Avoid duplicates
                                entries.append(current_description)
                                identifiers.append(current_identifier)
                            current_identifier = None
                            current_description = None
            except subprocess.CalledProcessError:
                continue
        
        return entries, identifiers
    
    except Exception as e:
        print_error(f"Failed to enumerate boot entries: {e}")
        return [], []

def get_current_windows_default_os():
    try:
        output = subprocess.check_output(["bcdedit"], text=True)
        for line in output.splitlines():
            if "default" in line.lower() and "identifier" in line.lower():
                return line.split()[-1]
        return None
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get current default OS: {e}")
        return None

def set_windows_default_os(identifier):
    try:
        subprocess.run(["bcdedit", "/default", identifier], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set default OS: {e}")
        return False

# --- macOS Specific Functions ---
def get_macos_boot_entries():
    entries = []
    identifiers = []
    
    try:
        # Get current boot volume
        current_boot = subprocess.check_output(["diskutil", "info", "/"], text=True)
        current_id = None
        for line in current_boot.splitlines():
            if "Device Identifier:" in line:
                current_id = line.split(":")[1].strip()
                break
        
        # Get all bootable volumes as binary plist
        output = subprocess.check_output(["diskutil", "list", "-plist"])
        plist_data = plistlib.loads(output)
        
        for disk in plist_data.get("AllDisksAndPartitions", []):
            if disk.get("MountPoint") == "/":
                disk_name = disk.get("VolumeName", "Macintosh HD")
                entries.append(f"macOS ({disk_name})")
                identifiers.append(current_id)
            elif disk.get("Content") == "Apple_APFS":
                for partition in disk.get("Partitions", []):
                    if partition.get("Content") == "Apple_APFS":
                        vol_name = partition.get("VolumeName", "Untitled")
                        vol_id = partition.get("DeviceIdentifier")
                        if vol_id and vol_name:
                            entries.append(f"macOS ({vol_name})")
                            identifiers.append(vol_id)
        
        # Check for Boot Camp
        try:
            bootcamp_output = subprocess.check_output(
                ["system_profiler", "SPSoftwareDataType"], 
                text=True,
                stderr=subprocess.DEVNULL
            )
            if "Boot Camp" in bootcamp_output:
                entries.append("Windows (Boot Camp)")
                identifiers.append("BOOTCAMP")
        except:
            pass
        
        return entries, identifiers
    
    except Exception as e:
        print_error(f"Failed to enumerate boot entries: {e}")
        return [], []

def get_current_macos_default_os():
    try:
        output = subprocess.check_output(["systemsetup", "-getstartupdisk"], text=True)
        return output.split(":")[1].strip() if ":" in output else None
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get current default OS: {e}")
        return None

def set_macos_default_os(disk_identifier):
    try:
        if disk_identifier == "BOOTCAMP":
            # For Boot Camp, we need to use bless
            subprocess.run(["sudo", "bless", "--mount", "/Volumes/BOOTCAMP", "--setBoot", "--legacy"], check=True)
        else:
            # For regular macOS volumes
            subprocess.run(["sudo", "bless", "--mount", f"/dev/{disk_identifier}", "--setBoot"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set default OS: {e}")
        return False

def reboot_macos():
    try:
        subprocess.run(["sudo", "shutdown", "-r", "now"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to reboot: {e}")
        return False

# --- Main Menu ---
def main():
    # Check if we should launch in new terminal
    if "--no-terminal-launch" not in sys.argv:
        launch_in_new_terminal()

    
    print_banner()
    
    try:
        current_os = platform.system()
        if current_os not in ("Linux", "Windows", "Darwin"):
            print_error("This script only runs on Linux, Windows, or macOS systems.")
            sys.exit(1)
            
        exit_if_not_admin()

        if current_os == "Linux":
            global GRUB_UPDATE_CMD
            GRUB_UPDATE_CMD = get_grub_update_cmd()
            if not ensure_os_prober_enabled():
                print_warning("Continuing with limited functionality")
            entries = get_linux_boot_entries()
            identifiers = None
            current_default = get_current_linux_default_os()
        elif current_os == "Windows":
            entries, identifiers = get_windows_boot_entries()
            current_default_id = get_current_windows_default_os()
            current_default = entries[identifiers.index(current_default_id)] if current_default_id and current_default_id in identifiers else "Unknown"
        else:  # macOS
            entries, identifiers = get_macos_boot_entries()
            current_default_id = get_current_macos_default_os()
            current_default = next((entry for entry, ident in zip(entries, identifiers) if ident == current_default_id), None)

        if not entries:
            print_error("No boot entries found. Cannot continue.")
            return

        print(f"\n{Fore.CYAN}📜 Available Boot Entries:{Style.RESET_ALL}")
        if current_os == "Linux":
            for idx, entry in enumerate(entries):
                current_marker = " (Current Default)" if entry == current_default else ""
                print(f"  {idx + 1}. {entry}{current_marker}")
        else:  # Windows or macOS
            for idx, (entry, identifier) in enumerate(zip(entries, identifiers)):
                if current_os == "Windows":
                    current_marker = " (Current Default)" if identifier == current_default_id else ""
                else:  # macOS
                    current_marker = " (Current Default)" if identifier == current_default_id else ""
                print(f"  {idx + 1}. {entry}{current_marker}")

        print(f"""\n{Fore.CYAN}⚙️  Options:
  1. Set default boot OS
  2. Flip OS
  3. Exit{Style.RESET_ALL}""")

        try:
            option = int(input("\nChoose an option (1-3): ").strip())
            if option not in [1, 2, 3]:
                print_error("Invalid option.")
                return
            if option == 3:
                print_info("Exiting OS Flip.")
                sys.exit(0)
                return

            choice = int(input("Select OS number: ").strip()) - 1
            if choice < 0 or choice >= len(entries):
                print_error("Invalid OS selection.")
                return

            if current_os == "Linux":
                selected_os = entries[choice]
                print_info(f"Selected: {selected_os}")

                if option == 1:
                    print_info(f"Current default: {current_default}")
                    if set_linux_default_os(selected_os):
                        print_success(f"Default OS set to: {selected_os}")
                        reboot = input("🔁 Flip now? (y/N): ").strip().lower()
                        if reboot == "y":
                            subprocess.run(["reboot"])
                elif option == 2:
                    print_info(f"Flip into: {selected_os}")
                    # Use title instead of index
                    grub_reboot_cmd = shutil.which("grub-reboot") or shutil.which("grub2-reboot")
                    
                    if not grub_reboot_cmd:
                        print_error("❌ Neither 'grub-reboot' nor 'grub2-reboot' found")
                        print_info("💡 Install with: sudo apt install grub2-common (Debian) or sudo dnf install grub2-tools (Fedora)")
                        return

                    try:
                        # Pass the exact menu entry title
                        subprocess.run([grub_reboot_cmd, selected_os], check=True)
                        print_success("Temporary boot set. Rebooting...")
                        subprocess.run(["reboot"])
                    except subprocess.CalledProcessError as e:
                        print_error(f"Failed to set temporary boot: {e}")
                        
            elif current_os == "Windows":
                selected_os = entries[choice]
                selected_id = identifiers[choice]
                print_info(f"Selected: {selected_os}")

                if option == 1:
                    print_info(f"Current default: {current_default}")
                    if set_windows_default_os(selected_id):
                        print_success(f"Default OS set to: {selected_os}")
                        reboot = input("🔁 Flip now? (y/N): ").strip().lower()
                        if reboot == "y":
                            subprocess.run(["shutdown", "/r", "/t", "0"])
                elif option == 2:
                    print_info(f"Rebooting into: {selected_os}...")
                    if set_windows_default_os(selected_id):
                        subprocess.run(["shutdown", "/r", "/t", "0"])
            else:  # macOS
                selected_os = entries[choice]
                selected_id = identifiers[choice]
                print_info(f"Selected: {selected_os}")

                if option == 1:
                    print_info(f"Current default: {current_default}")
                    if set_macos_default_os(selected_id):
                        print_success(f"Default OS set to: {selected_os}")
                        reboot = input("🔁 Flip now? (y/N): ").strip().lower()
                        if reboot == "y":
                            reboot_macos()
                elif option == 2:
                    print_info(f"Rebooting into: {selected_os}...")
                    if set_macos_default_os(selected_id):
                        reboot_macos()

        except ValueError:
            print_error("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
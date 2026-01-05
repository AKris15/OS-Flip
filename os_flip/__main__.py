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

from arguments import *
args = parser.parse_args()

# Color Codes
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

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
        print(f"{RED}⚠️ Cannot write to log at {path}. Logging disabled.{RESET}")

# --- Print Helpers ---
def print_success(msg): print(f"{GREEN}✅ {msg} {RESET}"); log(f"SUCCESS: {msg}")
def print_info(msg): print(f"{CYAN}ℹ️  {msg} {RESET}"); log(f"INFO: {msg}")
def print_warning(msg): print(f"{YELLOW}⚠️  {msg} {RESET}"); log(f"WARNING: {msg}")
def print_error(msg): print(f"{RED}❌ {msg} {RESET}"); log(f"ERROR: {msg}")

# --- Banner ---
def print_banner():
    if platform.system() == "Windows":
        color = BLUE
        os_name = "Windows"
    elif platform.system() == "Darwin":
        color = MAGENTA
        os_name = "macOS"
    else:  # Linux
        color = RED
        os_name = "Linux"
    
    banner = rf"""{RED}
   ____   _____          ______ _      _____ _____ 
  / __ \ / ____|        |  ____| |    |_   _|  __ \
 | |  | | (___    ___   | |__  | |      | | | |__) |
 | |  | |\___ \         |  __| | |      | | |  ___/ 
 | |__| |____) |        | |    | |____ _| |_| |     
  \____/|_____/         |_|    |______|_____|_|   
    
{RESET}                Welcome to OS FLIP 
                            By - AK({os_name})
"""
    print(banner)
    log(f"Launched OS Flip ({os_name})")

# --- Launches a New Terminal ---
def launch_in_new_terminal():
    """Try to launch the script in the user's default terminal, or fall back to known list."""
    current_os = platform.system()
    script_path = os.path.abspath(__file__)
    
    if current_os == "Windows":
        subprocess.Popen(f'start cmd /k python "{script_path}" -nt', shell=True)
        sys.exit(0)
    elif current_os == "Darwin":
        subprocess.Popen([
            "osascript",
            "-e", f'tell app "Terminal" to do script "python3 \'{script_path}\' -nt"'
        ])
        sys.exit(0)
    elif current_os == "Linux":
        # 1. Define the executable and arguments for launching the script
        python_executable = sys.executable
        script_command = [python_executable, script_path, "-nt"] 
        
        # 2. Check environment for user-defined default terminal ($TERMINAL)
        default_term_cmd = os.environ.get("TERMINAL")
        if default_term_cmd and shutil.which(default_term_cmd):
            print_info(f"Attempting to launch in default terminal: {default_term_cmd}")
            try:
                # Most default terminals will work with the simple -e or a specific command format
                # We'll use the safe, separate-argument format first.
                subprocess.Popen([default_term_cmd, "-e"] + script_command)
                sys.exit(0)
            except Exception as e:
                print_warning(f"Failed to launch with user's default terminal ({default_term_cmd}): {e}. Falling back...")
        
        # 3. Fallback to the comprehensive list (your original logic)
        terminals = [
            "ptyxis", "kitty", "ghostty", "alacritty", "wezterm", "foot", "st", "gnome-terminal", "konsole", 
            "xfce4-terminal", "mate-terminal", "tilix", "terminator", "lxterminal", 
            "deepin-terminal", "qterminal", "eterm", "mlterm", "urxvt", "xterm"
        ]

        for term in terminals:
            if shutil.which(term):
                try:
                    # Group 1: Terminals that typically require the command as a single, quoted shell string
                    if term in ("gnome-terminal", "konsole", "xfce4-terminal", "mate-terminal", "lxterminal", "deepin-terminal", "qterminal", "eterm", "mlterm"):
                        # We use sys.executable and quotes for shell compatibility
                        full_cmd_string = f'{python_executable} "{script_path}" -nt'
                        subprocess.Popen([term, "-e", full_cmd_string])
                    
                    # Group 2: Terminals that require the command and arguments as separate items
                    elif term in ("alacritty", "kitty", "foot", "wezterm", "ghostty", "st", "tilix", "terminator", "ptyxis", "urxvt", "xterm"):
                        # This is the safest way to pass the command for modern terminals
                        subprocess.Popen([term, "-e"] + script_command)
                    
                    else:
                        # Default fallback using separate items (safer approach)
                        subprocess.Popen([term, "-e"] + script_command)
                        
                    sys.exit(0)
                except Exception as e:
                    print_warning(f"Failed to launch with {term}: {e}")
        
        # 4. Final Fallback prompt
        print_warning("⚠️ No supported terminal emulator found.")
        fallback = input("Would you like to run this script in the current terminal instead? (y/N): ").strip().lower()
        if fallback == "y":
            # Just continue running in this terminal (no recursion!)
            return
        else:
            print_error("Please install a terminal emulator (e.g., kitty or gnome-terminal).")
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
    if Path("/etc/arch-release").exists():
        print_info("Detected Arch Linux/derivative.")
        return "grub-mkconfig -o /boot/grub/grub.cfg"
    elif Path("/etc/debian_version").exists():
        print_info("Detected Debian/Ubuntu/derivative.")
        return "update-grub"
    elif Path("/etc/redhat-release").exists() or "fedora" in platform.platform().lower():
        print_info("Detected RedHat/Fedora/derivative.")
        return "grub2-mkconfig -o /boot/grub2/grub.cfg"
        
    print_error("Unsupported Linux distribution. Cannot determine GRUB update command.")
    sys.exit(1)

def update_grub():
    global GRUB_UPDATE_CMD
    try:
        subprocess.run(GRUB_UPDATE_CMD, shell=True, check=True)
        print_success("GRUB configuration updated.")
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

    try:
        with open("/etc/default/grub", "r") as f:
            lines = f.readlines()
    except Exception as e:
        print_error(f"Failed to read /etc/default/grub: {e}")
        return False

    updated = False
    for i, line in enumerate(lines):
        if line.startswith("GRUB_DISABLE_OS_PROBER="):
            lines[i] = "GRUB_DISABLE_OS_PROBER=false\n"
            updated = True
            break

    if not updated:
        lines.append("\nGRUB_DISABLE_OS_PROBER=false\n")

    try:
        with open("/etc/default/grub", "w") as f:
            f.writelines(lines)
    except PermissionError as e:
        print_error(f"Failed to modify GRUB config: {e}")
        return False

    print_success("os-prober enabled in /etc/default/grub.")
    print_info("Updating GRUB entries (running os-prober)...")
    try:
        subprocess.run(["os-prober"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return update_grub()
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to run os-prober directly: {e}. Attempting GRUB update anyway.")
        return update_grub()
        
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
                        parts = line.split("'")
                        if len(parts) > 1:
                            title = parts[1]
                        else:
                            parts = line.split('"')
                            if len(parts) > 1:
                                title = parts[1]
                            else:
                                continue # Skip lines that don't match expected format
                                
                        if title not in seen:
                            entries.append(title)
                            seen.add(title)
        except Exception as e:
            print_warning(f"Failed to read GRUB config at {grub_path}: {e}")
        
    bls_dir = Path("/boot/loader/entries")
    if bls_dir.exists():
        for entry in bls_dir.glob("*.conf"):
            try:
                with open(entry) as f:
                    for line in f:
                        if line.startswith("title"):
                            title = line.strip().split(" ", 1)[1]
                            if title not in seen:
                                entries.append(title)
                                seen.add(title)
                            break
            except Exception as e:
                print_warning(f"Failed to read BLS entry {entry}: {e}")


    if not entries:
        print_error("No boot entries found in standard locations.")
    return entries

def get_current_linux_default_os():
    try:
        with open("/etc/default/grub", "r") as f:
            for line in f:
                if line.startswith("GRUB_DEFAULT="):
                    return line.split("=", 1)[1].strip().strip('"')
    except Exception as e:
        print_warning(f"Could not read default GRUB entry: {e}")
        return None

def set_linux_default_os(entry_name):
    try:
        with open("/etc/default/grub", "r") as f:
            lines = f.readlines()
    except Exception as e:
        print_error(f"Failed to read /etc/default/grub: {e}")
        return False

    found = False
    for i, line in enumerate(lines):
        if line.startswith("GRUB_DEFAULT="):
            lines[i] = f'GRUB_DEFAULT={entry_name}\n'
            found = True
            break
    
    if not found:
        lines.append(f'\nGRUB_DEFAULT="{entry_name}"\n')

    try:
        with open("/etc/default/grub", "w") as f:
            f.writelines(lines)
    except PermissionError as e:
        print_error(f"Failed to write to /etc/default/grub: {e}")
        return False

    return update_grub()

# --- Windows Specific Functions ---
def get_windows_boot_entries():
    entries = []
    identifiers = []
    
    try:
        commands = [
            ["bcdedit", "/enum", "Firmware"],
            ["bcdedit", "/enum", "OSLOADER"],
            ["bcdedit"]
        ]
        
        for cmd in commands:
            if entries:
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
                            if current_description not in entries:
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
        subprocess.run(["bcdedit", "/default", identifier], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set default OS: {e}")
        return False

# --- macOS Specific Functions ---
def get_macos_boot_entries():
    entries = []
    identifiers = []
    
    try:
        # Get all bootable volumes as binary plist
        output = subprocess.check_output(["diskutil", "list", "-plist", "internal"])
        plist_data = plistlib.loads(output)
        
        current_boot_id = None
        try:
            current_boot_info = subprocess.check_output(["diskutil", "info", "/"], text=True)
            for line in current_boot_info.splitlines():
                if "Device Identifier:" in line:
                    current_boot_id = line.split(":")[1].strip()
                    break
        except:
            pass
        
        # Iterate over partitions to find bootable volumes
        for disk in plist_data.get("AllDisksAndPartitions", []):
            if disk.get("Content") == "Apple_APFS":
                for partition in disk.get("Partitions", []):
                    # Look for APFS Volumes
                    if partition.get("Content") in ("Apple_APFS_Volume", "Apple_Boot"): 
                        vol_name = partition.get("VolumeName", "Untitled")
                        vol_id = partition.get("DeviceIdentifier")
                        
                        if vol_id and vol_name and vol_id not in identifiers:
                            # Only include macOS volumes (skip recovery, preboot, etc. unless they are the current boot)
                            if vol_name.lower().startswith("macintosh hd") or vol_id == current_boot_id:
                                entries.append(f"macOS ({vol_name})")
                                identifiers.append(vol_id)
        
        # Check for Boot Camp
        try:
            bootcamp_output = subprocess.check_output(
                ["diskutil", "list", "BOOTCAMP"], 
                text=True,
                stderr=subprocess.DEVNULL
            )
            if "BOOTCAMP" in bootcamp_output and "BOOTCAMP" not in identifiers:
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
        # Returns a descriptive path, e.g., "/System/Library/CoreServices/boot.efi" or "disk0s2"
        output = subprocess.check_output(["systemsetup", "-getstartupdisk"], text=True)
        return output.split(":")[1].strip() if ":" in output else None
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get current default OS: {e}")
        return None

def set_macos_default_os(disk_identifier):
    try:
        if disk_identifier == "BOOTCAMP":
            # For Boot Camp, we bless the volume mount point
            subprocess.run(["sudo", "bless", "--mount", "/Volumes/BOOTCAMP", "--setBoot"], check=True)
        else:
            # Find the mount point for the device identifier
            mount_point = None
            try:
                disk_info = subprocess.check_output(["diskutil", "info", disk_identifier], text=True)
                for line in disk_info.splitlines():
                    if "Mount Point:" in line:
                        mount_point = line.split(":")[1].strip()
                        break
            except Exception as e:
                print_error(f"Failed to find mount point for {disk_identifier}: {e}")
                return False

            if mount_point:
                # Bless the mount point
                subprocess.run(["sudo", "bless", "--mount", mount_point, "--setBoot"], check=True)
            else:
                print_error(f"Could not determine mount point for identifier {disk_identifier}. Cannot bless.")
                return False
                
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
class MAIN_MENU:
    def __init__(self):
        self.current_os = platform.system()
        self.current_default = None
        self.entries = None
        self.identifiers = None
        self.current_default_id = None
        self.current_default_display_name = None

    def os_check(self):
        if self.current_os not in ("Linux", "Windows", "Darwin"):
            print_error("This script only runs on Linux, Windows, or macOS systems.")
            sys.exit(1)
            
        exit_if_not_admin()

    def get_boot_entires(self):
        if self.current_os == "Linux":
            global GRUB_UPDATE_CMD
            GRUB_UPDATE_CMD = get_grub_update_cmd()
            if not ensure_os_prober_enabled():
                print_warning("Continuing with limited functionality")
            self.entries = get_linux_boot_entries()
            self.current_default = get_current_linux_default_os()
        elif self.current_os == "Windows":
            self.entries, self.identifiers = get_windows_boot_entries()
            self.current_default_id = get_current_windows_default_os()
            self.current_default = self.entries[self.identifiers.index(self.current_default_id)] if self.current_default_id and self.current_default_id in self.identifiers else "Unknown"
        else:  # macOS
            self.entries, self.identifiers = get_macos_boot_entries()
            self.current_default_display_name = get_current_macos_default_os()
            # Note: macOS default is complex. We use the display name for comparison.
            self.current_default = self.current_default_display_name

    def show_boot_entries(self):
        if self.current_os == "Linux":
            for idx, entry in enumerate(self.entries):
                current_marker = " (Current Default)" if entry == self.current_default else ""
                print(f"  {idx + 1}. {entry}{current_marker}")
        else:  # Windows or macOS
            for idx, (entry, identifier) in enumerate(zip(self.entries, self.identifiers)):
                current_marker = ""
                if self.current_os == "Windows":
                    current_marker = " (Current Default)" if identifier == self.current_default_id else ""
                elif self.current_os == "Darwin":
                    # Check if the entry name is contained in the descriptive current default path
                    if identifier == "BOOTCAMP" and "BOOTCAMP" in self.current_default_display_name:
                        current_marker = " (Current Default)"
                    elif identifier != "BOOTCAMP" and identifier in self.current_default_display_name:
                        current_marker = " (Current Default)"

                print(f"  {idx + 1}. {entry}{current_marker}")


class Operation:
    def __init__(self, menu, choice):
        self.menu = menu
        self.selected_os = menu.entries[choice]
        
        if menu.identifiers:
            self.selected_id = menu.identifiers[choice]
        else:
            self.selected_id = None  
        
    def windows_set_default(self):
        print_info(f"Current default: {self.menu.current_default}")
        if set_windows_default_os(self.selected_id):
            print_success(f"Default OS set to: {self.selected_os}")
            reboot = input("🔁 Flip now? (y/N): ").strip().lower()
            if reboot == "y":
                subprocess.run(["shutdown", "/r", "/t", "0"])

    def windows_flip(self):
        print_info(f"Rebooting into: {self.selected_os}...")
        if set_windows_default_os(self.selected_id):
            subprocess.run(["shutdown", "/r", "/t", "0"])

    def macos_set_default(self):
        print_info(f"Current default: {self.menu.current_default_display_name}")
        if set_macos_default_os(self.selected_id):
            print_success(f"Default OS set to: {self.selected_os}")
            reboot = input("🔁 Flip now? (y/N): ").strip().lower()
            if reboot == "y":
                reboot_macos()

    def macos_flip(self):
        print_info(f"Rebooting into: {self.selected_os} (One-time and default boot are the same on macOS)...")
        if set_macos_default_os(self.selected_id):
            reboot_macos()

    def linux_set_default(self):
        print_info(f"Current default: {self.menu.current_default}")
        if set_linux_default_os(str(choice)):
            print_success(f"Default OS set to: {self.selected_os}")
            reboot = input("🔁 Flip now? (y/N): ").strip().lower()
            if reboot == "y":
                subprocess.run(["reboot"])

    def linux_flip(self):
        print_info(f"Flip into: {self.selected_os}")
        grub_reboot_cmd = shutil.which("grub-reboot") or shutil.which("grub2-reboot")
        
        if not grub_reboot_cmd:
            print_error("❌ Neither 'grub-reboot' nor 'grub2-reboot' found")
            print_info("💡 Install with: e.g., sudo apt install grub2-common (Debian) or sudo pacman -S grub (Arch)")
            return

        try:
            subprocess.run([grub_reboot_cmd, self.selected_os], check=True)
            print_success("Temporary boot set. Rebooting...")
            subprocess.run(["reboot"])
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to set temporary boot: {e}")

def list_boot_entires():
    menu = MAIN_MENU()
    menu.os_check()
    menu.get_boot_entires()
    menu.show_boot_entries()
    sys.exit(0)

def run_operation():
    if not args.no_terminal and not sys.stdin.isatty():
        launch_in_new_terminal()

    menu = MAIN_MENU()
    menu.os_check()
    menu.get_boot_entires()

    if not menu.entries:
        print_error("No boot entries found.")
        sys.exit(1)

    menu.show_boot_entries()

    # ---- FLIP ----
    if args.flip is not None:
        choice = args.flip-1

        if not (0 <= choice < len(menu.entries)):
            print_error("Invalid OS selection.")
            sys.exit(1)

        op = Operation(menu, choice)

        if menu.current_os == "Linux":
            op.linux_flip()
        elif menu.current_os == "Windows":
            op.windows_flip()
        else:
            op.macos_flip()

    # ---- SET DEFAULT ----
    elif args.set_default is not None:
        choice = args.set_default - 1

        if not (0 <= choice < len(menu.entries)):
            print_error("Invalid OS selection.")
            sys.exit(1)

        op = Operation(menu, choice)

        if menu.current_os == "Linux":
            op.linux_set_default()
        elif menu.current_os == "Windows":
            op.windows_set_default()
        else:
            op.macos_set_default()

def files_clean():
    print("function not implemened yet")

def default():
    menu = MAIN_MENU()
    menu.os_check()
    menu.get_boot_entires()

    if not menu.entries:
        print_error("No boot entries found.")
        sys.exit(1)

    menu.show_boot_entries()

    choice = int(input(f"""\n Enter the value for the OS you want to boot into :
    (eg :   3. Arch Linux (6.17.11-300.x86_64)), enter -> 3: """))
    op = Operation(menu, choice - 1)

    if menu.current_os == "Linux":
        op.linux_flip()
    elif menu.current_os == "Windows":
        op.windows_flip()
    else:
        op.macos_flip()

def main():
    print_banner()

    try:
        if args.clean:
            files_clean()
        
        elif args.list:
            list_boot_entires()

        elif args.flip is not None or args.set_default is not None:
            run_operation()

        else:
            default()

    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user.")
        sys.exit(1)

    except Exception as e:
        print_error(f"An Unexpected error occurred: {e}")
        log(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


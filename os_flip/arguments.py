import argparse

# Argument parser configuration

# OS-Flip is a CLI utility to manage GRUB2 boot preferences on Linux systems.
# This parser defines all supported command-line flags and their behavior.

parser = argparse.ArgumentParser(
    prog='OS-Flip',
    usage=None,
    prefix_chars='-',
    description="""OS Flip is a Python utility that helps manage GRUB2 boot preferences on Linux.
      Features : 
      * List bootable operating systems 
      * Configure the default boot option 
      * Perform a one-time boot into another OS """,
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Created by : https://akris.is-a.dev ",
    color=True
)

# List available boot entries
# Example: -l or --list
parser.add_argument(
    '-l', '--list',
    action='store_true',
    help='List all detected GRUB boot entries'
)

# Run without spawning a new terminal window
# Useful when running from scripts or minimal environments
parser.add_argument(
    '-nt', '--no-terminal',
    action='store_true',
    help='Run without opening a new terminal window'
)

# Set the default OS for future boots
# Example: -sd or --set-default 2
parser.add_argument(
    '-sd', '--set-default',
    type=int,
    metavar='INDEX',
    help='Set default boot entry by index (use --list to see indices)'
)

# One-time boot into a selected OS (does not change default)
# Example: -f or --flip 1
parser.add_argument(
    '-f', '--flip',
    type=int,
    metavar='INDEX',
    help='Temporarily boot into selected OS (one-time)'
)

# Cleanup utility: remove logs and/or backups
# Example: -c or --clean {l,b.lb}
parser.add_argument(
    '-cl', '--clean',
    choices=['l', 'b', 'lb'],
    metavar='{l,b,lb}',
    help=(
        "Clean OS-Flip generated files:\n"
        "  l   - remove logs only\n"
        "  b   - remove backups only\n"
        "  lb  - remove both logs and backups"
    )
)

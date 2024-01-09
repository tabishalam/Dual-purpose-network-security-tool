import colors
import psutil
import subprocess


# Gets the list of interfaces with full details
def get_interfaces():
    try:
        interfaces_list_full = psutil.net_if_addrs()
        return interfaces_list_full
    except Exception as e:
        print(f"{colors.RED}Error: {e}{colors.RESET}")


# Gets interfaces name
def get_interfaces_name():
    try:
        return list(psutil.net_if_addrs().keys())
    except Exception as e:
        print(f"{colors.RED}Error: {e}{colors.RESET}")


# Print interfaces
def print_interfaces(interfaces):
    count = 0

    for interface in interfaces:
        print(f" {count}. {interface}")
        count += 1


# Change interface mode to monitor mode...
def to_monitor_mode(interface):
    command = "sudo airmon-ng start"
    try:
        subprocess.run([command, interface])
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to put interface in monitor mode!!!{colors.RESET}")
    else:
        print(f"{colors.GREEN}Monitor mode enabled for selected interface...{colors.RESET}")


# Reverse interface mode to monitor mode
def reverse_monitor_mode(interface):
    command = "sudo airmon-ng stop"
    try:
        subprocess.run([command, interface])
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to remove interface from monitor mode{colors.RESET}")
    else:
        print(f"{colors.GREEN}Monitor mode disabled!!!...{colors.RESET}")
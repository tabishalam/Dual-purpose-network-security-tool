import psutil
import subprocess

from Style import Colors
from Utils import Terminal


# Return list of interfaces with full details
def get_interfaces():
    try:
        interfaces_list_full = psutil.net_if_addrs()
        return interfaces_list_full
    
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")


# Return interfaces name
def get_interfaces_name():
    try:
        return list(psutil.net_if_addrs().keys())

    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")


# Print interfaces
def display_interfaces(interfaces):
    count = 0

    for interface in interfaces:
        print(f" {count}. {interface}")
        count = count + 1


# Change interface mode to monitor mode...
def to_monitor_mode(interface):
    try:
        subprocess.run(["sudo", "airmon-ng", "start", interface])
        print(f"{Colors.DEFAULT_COLOR}Monitor mode enabled for selected interface...{Colors.RESET}")

    except subprocess.CalledProcessError:
        print(f"{Colors.RED}Failed to put interface in monitor mode!!!{Colors.RESET}")


# Reverse interface mode to monitor mode
def reverse_monitor_mode(interface):
    try:
        subprocess.run("sudo airmon-ng stop" + interface)
        print(f"{Colors.GREEN}Monitor mode disabled!!!...{Colors.RESET}")

    except subprocess.CalledProcessError:
        print(f"{Colors.RED}Failed to remove interface from monitor mode{Colors.RESET}")


def select_interface():
    interfaces_list = None
    interface_id = None

    interfaces = get_interfaces_name()
    display_interfaces(interfaces)

    print(f"\n {Colors.DARK_YELLOW}Note: Please select interface that supports monitor mode.{Colors.RESET}")
    interface_id = int(input(" Select an interface (e.g: 0, 1): "))
    SELECTED_INTERFACE = interfaces[interface_id]

    Terminal.clear() # Clear terminal

    print(f"{Colors.YELLOW}Putting interfaces into monitor mode...{Colors.GREEN}")
    to_monitor_mode(SELECTED_INTERFACE)

    # Selecting interface automatically after changing mode of the interface as with some adapter name changes when using monitor mode
    interfaces = get_interfaces_name()
    SELECTED_INTERFACE = interfaces[interface_id]
    
    Terminal.clear() # Clear terminal
    return SELECTED_INTERFACE

import style.colors as colors
import psutil
import subprocess
import tool_functions.clear_terminal as clear_terminal


# Global Variable
SELECTED_INTERFACE = ""



# Return list of interfaces with full details
def get_interfaces():
    try:
        interfaces_list_full = psutil.net_if_addrs()
        return interfaces_list_full
    except Exception as e:
        print(f"{colors.RED}Error: {e}{colors.RESET}")


# Return interfaces name
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
    try:
        subprocess.run(["sudo", "airmon-ng", "start", interface])
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to put interface in monitor mode!!!{colors.RESET}")
    else:
        print(f"{colors.DEFAULT_COLOR}Monitor mode enabled for selected interface...{colors.RESET}")


# Reverse interface mode to monitor mode
def reverse_monitor_mode(interface):
    try:
        subprocess.run("sudo airmon-ng stop" + interface)
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to remove interface from monitor mode{colors.RESET}")
    else:
        print(f"{colors.GREEN}Monitor mode disabled!!!...{colors.RESET}")


def select_interface():
    # ******************* Variables *******************
    interfaces_list = None
    interface_id = None

    # ******************* Selecting and setting up interface for further uses... *******************
    interfaces = get_interfaces_name()
    print_interfaces(interfaces)

    print(f"\n {colors.DARK_YELLOW}Note: Please select interface that supports monitor mode.{colors.RESET}")
    interface_id = int(input(" Select an interface (e.g: 0, 1): "))
    SELECTED_INTERFACE = interfaces[interface_id]

    clear_terminal

    print(f"{colors.YELLOW}Putting interfaces into monitor mode...{colors.GREEN}")
    to_monitor_mode(SELECTED_INTERFACE)

    # Selecting interface automatically after changing mode of the interface as with some adapter name changes when using monitor mode
    interfaces = get_interfaces_name()
    SELECTED_INTERFACE = interfaces[interface_id]
    
    clear_terminal
    return SELECTED_INTERFACE

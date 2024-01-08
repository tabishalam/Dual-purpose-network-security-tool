import colors
import psutil
import subprocess


# Return list of interfaces with full details
def get_interfaces():
    try:
        interfaces_list_full = psutil.net_if_addrs()
        # interfaces_name = list(interfaces_list_full.keys())
        #
        # # Removes the first interface which is eth0
        # if interfaces_name:
        #     first_interface = interfaces_name[0]
        #     del interfaces_list_full[first_interface]

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
        print(f"{colors.GREEN}Monitor mode enabled for selected interface...{colors.RESET}")


# Reverse interface mode to monitor mode
def reverse_monitor_mode(interface):
    try:
        subprocess.run("sudo airmon-ng stop" + interface)
    except subprocess.CalledProcessError:
        print(f"{colors.RED}Failed to remove interface from monitor mode{colors.RESET}")
    else:
        print(f"{colors.GREEN}Monitor mode disabled!!!...{colors.RESET}")
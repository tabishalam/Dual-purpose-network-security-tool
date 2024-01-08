import style.colors as colors
import wifi.wifi_scanner as wifi_scanner
import tool_functions.clear_terminal as clear_terminal
import tool_functions.tools_management as tools_management
import tool_functions.interface_management as interface_management
import wifi.network_scanner as network_scanner
import arp.arp_spoof as arp_spoof

SELECTED_INTERFACE = ""


def main_options():
    print("1. Scan for targets")
    print("2. Show connected Devices")
    print("3. Arp spoof attack")
    print("0. Exit")

    selected_option = int(input("Select any option: "))

    match selected_option:
        case 1:
            wifi_scanner.start_scan(SELECTED_INTERFACE)
        case 2:
            network_scanner.scan()
        case 3:
            arp_spoof.start_spoof()
        case _:
            print("Select a valid option...")
            main_options()


def main():
    global SELECTED_INTERFACE

    clear_terminal # Clears terminal

    # Checking and installing required Tools/Packages
    print(f"{colors.YELLOW}Checking if required application is installed......{colors.RESET} \n")
    tools_management.manage_tools()

    clear_terminal # Clears terminal

    # Select interface for futher use...
    SELECTED_INTERFACE = interface_management.select_interface()
    
    print(SELECTED_INTERFACE)
    
    clear_terminal # Clears terminal

    # Print options
    main_options()    

if __name__ == "__main__":
    main()
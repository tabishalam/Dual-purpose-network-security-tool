import os
from threading import Thread
import style.colors as colors
import utils.terminal as terminal
import arp.arp_spoofer as arp_spoofer
import wifi.nearby_wifi_scanner as wifi_scanner
import utils.tools_management as tools_management
import wifi.connected_devices as connected_devices
import utils.interface_management as interface_management


# Global variable
SELECTED_INTERFACE = "" # WiFi interface 
SELECTED_NETWORK = ""


# Options to show after wifi scanning completes
def wifi_scan_options():
    print("1. Capture Handshake")
    print("2. De-authenticate single clint")
    print("3. De-authenticate All clients")
    print("4. Go Back")
    print("5. Exit")

    selected_option = input("Select an option: ")

    match selected_option:
        case 1:
            pass

        case 2:
            pass

        case 3:
            pass

        case 4:
            pass

        case 5:
            pass


# Options for attacking mode
def attack_options():
    print("1. Scan for WiFi")
    print("2. Get all connected device")
    print("3. Arp Spoofing attack")
    
    selected_option = int(input("Select any option: "))

    terminal.clear() # Clears terminal

    match selected_option:
        case 1:
            wifi_scanner.start_scan(SELECTED_INTERFACE)
            terminal.clear()
            wifi_scanner.print_final_scan()
            wifi_scanner.select_network()

        case 2:
            connected_devices.start_scan(SELECTED_INTERFACE)
            
        case 3:
            arp_spoofer.start_spoof(SELECTED_INTERFACE)


# Main option to select operation mode of the tool
def main_option():
    print("1. Attack")
    print("2. Defend")
    
    selected_option = int(input("Select any option: "))

    terminal.clear() # Clears terminal

    
    match selected_option:
        case 1:
            terminal.clear()
            attack_options()

        case 2:
            terminal.clear() # Clears terminal
            pass
        
        case _:
            print(f"{colors.RED}Please select a valid option!!{colors.RESET}\n")
            main_option()


# Main function to control the flow of program
def main():
    global SELECTED_INTERFACE # Acccesing global variable
    
    terminal.clear() # Clears terminal
 
    # Checking and installing required Tools/Packages
    print(f"{colors.YELLOW}Checking if required application is installed......{colors.RESET} \n")
    tools_management.manage_tools()

    terminal.clear() # Clears terminal

    # Select interface for futher use...
    SELECTED_INTERFACE = interface_management.select_interface()    
    
    terminal.clear() # Clears terminal 

    # Print options
    main_option()    


if __name__ == "__main__":
    main()

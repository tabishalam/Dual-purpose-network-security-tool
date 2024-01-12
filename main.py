import style.colors as colors
import arp.arp_spoof as arp_spoof
import wifi.wifi_scanner as wifi_scanner
import utils.terminal as terminal
import wifi.get_connected_clients as get_connected_clients
import utils.tools_management as tools_management
import utils.interface_management as interface_management

# Global variable
SELECTED_INTERFACE = "" # WiFi interface 


# Options for attacking mode
def attack_options():
    print("1. Scan for WiFi")
    print("2. Get all connected device")
    print("3. Arp Spoofing attack")
    
    selected_option = int(input("Select any option: "))
    terminal.clear()

    match selected_option:
        case 1:
            wifi_scanner.start_scan(SELECTED_INTERFACE)
            
        case 2:
            get_connected_clients.start_scan()
            
        case 3:
            arp_spoof.start_spoof()


# Main option to select operation mode of the tool
def main_option():
    print("1. Attack")
    print("2. Defend")
    
    selected_option = int(input("Select any option: "))
    terminal.clear()

    
    match selected_option:
        case 1:
            attack_options()
        
        case 2:
            pass
        
        case _:
            print(f"{colors.RED}Please select a valid option!!{colors.RESET}\n")
            main_option()
            
            
# def main_options():
#     print("1. Scan for targets")
#     print("2. Show connected Devices")
#     print("3. Arp spoof attack")
#     print("0. Exit")

#     selected_option = int(input("Select any option: "))

#     match selected_option:
#         case 1:
#             wifi_scanner.start_scan(SELECTED_INTERFACE)
#         case 2:
#             network_scanner.scan()
#         case 3:
#             arp_spoof.start_spoof()
#         case _:
#             print("Select a valid option...")
#             main_options()


# Main function to control the flow of program
def main():
    global SELECTED_INTERFACE # Acccesing global variable

    terminal.clear()
 

    # Checking and installing required Tools/Packages
    print(f"{colors.YELLOW}Checking if required application is installed......{colors.RESET} \n")
    tools_management.manage_tools()

    terminal.clear() 

    # Select interface for futher use...
    SELECTED_INTERFACE = interface_management.select_interface()    
    
    # Clears terminal
    terminal.clear() 

    # Print options
    main_option()    

if __name__ == "__main__":
    main()

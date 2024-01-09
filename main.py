import style.colors as colors
import wifi.wifi_scanner as wifi_scanner
import utils.clear_terminal as clear_terminal
import utils.tools_management as tools_management
import utils.interface_management as interface_management
import wifi.network_scanner as network_scanner
import arp.arp_spoof as arp_spoof

# Global variable
SELECTED_INTERFACE = "" # WiFi interface 


# Main option to select operation mode of the tool
def main_option():
    print("1. Attack")
    print("2. Defend")
    
    selected_option = input("Select any option: ")
    
    match selected_option:
        case 1:
            clear_terminal
            attack_options()
        
        case 2:
            pass
        
        case _:
            clear_terminal
            print(f"{colors.RED}Please select a valid option!!{colors.RESET}\n")
            main_option()
            

# Options for attacking mode
def attack_options():
    print("1. Scan for WiFi")
    print("2. Get all connected device")
    print("3. Arp Spoofing attack")
    
    selected_option = input("Select any option: ")

    match selected_option:
        case 1:
            clear_terminal
            network_scanner.start_scan()
            
        case 2:
            clear_terminal
            network_scanner.start_scan()
            
        case 3:
            arp_spoof.start_spoof()
            
            
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

    clear_terminal 

    # Checking and installing required Tools/Packages
    print(f"{colors.YELLOW}Checking if required application is installed......{colors.RESET} \n")
    tools_management.manage_tools()

    clear_terminal 

    # Select interface for futher use...
    SELECTED_INTERFACE = interface_management.select_interface()    
    
    # Clears terminal
    clear_terminal 

    # Print options
    main_option()    

if __name__ == "__main__":
    main()

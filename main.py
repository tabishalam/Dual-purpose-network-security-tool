import sys
import style.colors as colors
import utils.terminal as terminal
import arp.arp_spoofer as arp_spoofer
import utils.tools_management as tools_management
import wifi.connected_devices as connected_devices
import utils.interface_management as interface_management


# Global variable
SELECTED_INTERFACE = "" # WiFi interface 
EXIT = False

def mactch_case(option_list, option):
    # First function match case option
    if option_list == 1:
        match option:
            case 1:
                attack_options()

            case 2:
                pass
            
            case _:
                print(f"{colors.RED}Please select a valid option!!{colors.RESET}\n")
                input("Press any key to try again!!!")
                terminal.clear()
                return True


    # Second function match case option
    if option_list == 2:
        match option:
            case 1:
                connected_devices.start_scan(SELECTED_INTERFACE)
                print("\n")

            case 2:
                arp_spoofer.start_spoof(SELECTED_INTERFACE)

            case 3:
                arp_spoofer.start_spoof(SELECTED_INTERFACE)

            case 4:
                arp_spoofer.start_spoof(SELECTED_INTERFACE)

            case 5:
                main_option()

            case 0:
                try:
                    sys.exit()
                finally:
                    print("[+] Program Stopped!!!")
                
            case _:
                print(f"{colors.RED}Please select a valid option!!{colors.RESET}\n")
                input("Press any key to try again!!!")
                terminal.clear()
                return True
            

# Options for attacking mode
# Option code 2
def attack_options():
    print("1. Get all connected device")
    print("2. Arp Spoofing attack")
    print("3. DNS Spoofing")
    print("4. Replace download file")
    print("5. Go Back")
    print("0. Exit")
    
    selected_option = int(input("Select any option: "))
    terminal.clear() # Clears terminal

    while EXIT != True:
        invalid_selection = mactch_case(2, selected_option)
        attack_options()


# Main option to select operation mode of the tool
# Option code 1
def main_option():
    print("1. Attack")
    print("2. Defend")
    
    selected_option = int(input("Select any option: "))
    terminal.clear() # Clears terminal

    while EXIT != True:
        invalid_selection = mactch_case(1, selected_option)
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

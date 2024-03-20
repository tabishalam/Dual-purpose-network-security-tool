import sys

from Style import Colors
from Network_Scanner import Network_Scanner
from Utils import Terminal, Tools_Management, Interface_Management
from ARP import ARP_Spoofer, Detector as ARP_Detector, DNS_Spoofer, File_Intercepter

# # Global variable
SELECTED_INTERFACE = "" # WiFi interface 
EXIT = False

def mactch_case(option_list, option):
    # First function match case option
    if option_list == 1:
        match option:
            case 1:
                attack_options()

            case 2:
                ARP_Detector.sniff(SELECTED_INTERFACE)
            
            case _:
                print(f"{Colors.RED}Please select a valid option!!{Colors.RESET}\n")
                input("Press any key to try again!!!")
                Terminal.clear()
                return True


    # Second function match case option
    if option_list == 2:
        match option:
            case 1:
                Network_Scanner.start_scan(SELECTED_INTERFACE)
                print("\n")

            case 2:
                ARP_Spoofer.start_spoof_sniff(SELECTED_INTERFACE)
            
            case 3:
                ARP_Spoofer.start_spoof(SELECTED_INTERFACE)

            case 4:
                DNS_Spoofer.start_spoofing()

            case 5:
                File_Intercepter.run()

            case 6:
                main_option()

            case 0:
                try:
                    sys.exit()
                finally:
                    print("[+] Program Stopped!!!")
                
            case _:
                print(f"{Colors.RED}Please select a valid option!!{Colors.RESET}\n")
                input("Press any key to try again!!!")
                Terminal.clear()
                return True
            

# Options for attacking mode
# Option code 2
def attack_options():
    print("1. Get all connected device")
    print("2. Arp Spoofing attack (ARP Spoofing and Data Sniffing)")
    print("3. Arp Spoofing attack (ARP Spoofing only)")
    print("4. DNS Spoofing")
    print("5. Replace download file")
    print("6. Go Back")
    print("0. Exit")
    
    selected_option = int(input("Select any option: "))
    Terminal.clear() # Clears Terminals

    while EXIT is not True:
        mactch_case(2, selected_option)
        attack_options()


# Main option to select operation mode of the tool
# Option code 1
def main_option():
    print("1. Attack")
    print("2. Defend")
    
    selected_option = int(input("Select any option: "))
    Terminal.clear() # Clears Terminal

    while EXIT is not True:
        mactch_case(1, selected_option)
        main_option()


# Main function to control the flow of program
def start_main():
    global SELECTED_INTERFACE
    Terminal.clear() # Clears terminal

    # Checking and installing required Tools/Packages
    print(f"{Colors.YELLOW}Checking if required application is installed......{Colors.RESET} \n")
    Tools_Management.manage_tools()
    Terminal.clear() # Clears terminal

    # Select interface for futher use...
    SELECTED_INTERFACE = Interface_Management.select_interface()
    Terminal.clear() # Clears terminal 

    # Print options
    main_option()    


if __name__ == "__main__":
    start_main()
    # Main = Main()
    # Main.start_main()

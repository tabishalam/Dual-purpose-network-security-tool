import subprocess
import time
import re
import os
import tabulate
import csv


TIMESTAMP = time.strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"scanned_wifi_{TIMESTAMP}" 


def print_scanned_result():
    rows = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f"{OUTPUT_FILE}-01.csv")

    # Opening the output file
    with open(file_path, "r") as raw_output:
    
        # Reading file with csv.reader() method
        csvreader = csv.reader(raw_output)
        header = next(csvreader)
        
        for row in csvreader:
            rows.append(row)

    print(header)
    print(rows)


def start_scan(SELECTED_INTERFACE):
    try:
        
        # Define the Airodump-ng command to run as a subprocess
        airodump_command = ["airodump-ng", "--output-format", "csv", "--write", OUTPUT_FILE, SELECTED_INTERFACE]
        
        # Start Airodump-ng as a subprocess
        airodump_process = subprocess.Popen(airodump_command)
        airodump_process.wait()

    except KeyboardInterrupt:
        try:
            print_scanned_result()
        except Exception as e:
            pass
        # print(e)

if __name__ == "__main__":
    selected_interface = "wlan0"  # Change this to your Wi-Fi interface
    start_scan(selected_interface)




    # try:
    #     # Read the captured data from the CSV file
    #     with open(file_path, "r") as data_file:
    #         wifi_data = data_file.read()

    #     # Parse the captured data (extracting BSSID and ESSID from the top section)
    #     top_section_match = re.search(r"BSSID,.*?ESSID, Key\n(.*?)\n\n", wifi_data, re.DOTALL)
    #     if top_section_match:
    #         top_section_data = top_section_match.group(1)
    #         top_networks = re.findall(r"([^,]+),[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,([^,]+),.*", top_section_data)

    #         # Display the discovered networks from the top section
    #         print("Top Section:")
    #         top_table = tabulate(top_networks, headers=["BSSID", "ESSID"], tablefmt="plain")
    #         print(top_table)

    #     # Parse the captured data (extracting Station MAC and Probed ESSIDs from the bottom section)
    #     bottom_section_match = re.search(r"Station MAC,.*?Probed ESSIDs\n(.*?)\n\n", wifi_data, re.DOTALL)
    #     if bottom_section_match:
    #         bottom_section_data = bottom_section_match.group(1)
    #         bottom_networks = re.findall(r"([^,]+),[^,]+,[^,]+,[^,]+,[^,]+,([^,]+),.*", bottom_section_data)

    #         # Display the discovered networks from the bottom section
    #         print("\nBottom Section:")
    #         bottom_table = tabulate(bottom_networks, headers=["Station MAC", "Probed ESSID"], tablefmt="plain")
    #         print(bottom_table)

    # except FileNotFoundError:
    #     print(f"File '{file_path}' not found.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")








# import os
# import time
# from scapy.all import *
# from tabulate import tabulate
# import clear_terminal

# # SSID - Name of the network
# # BSSID - MAC address of the network

# # Discovered network and their clients
# networks = {}

# def process_packet(packet):
#     if packet.haslayer(Dot11):
#         if packet.type == 0 and packet.subtype == 8:
#             # Beacon frame (packet.type = 0, packet.subtype = 8)
#             ssid = packet.info.decode("utf-8")
#             bssid = packet.addr2
#             channel = ord(packet[Dot11Elt:3].info[0])

#             if bssid not in networks:
#                 networks[bssid] = {"SSID": ssid, "Channel": channel, "Clients": set()}

#         elif packet.type == 0 and packet.subtype == 4:
#             # Probe request frame (packet.type = 0, packet.subtype = 4)
#             bssid = packet.addr1
#             client_mac = packet.addr2

#             if bssid in networks:
#                 networks[bssid]["Clients"].add(client_mac)

# def start_scan(SELECTED_INTERFACE):
#     try:
#         while True:
#             os.system('clear')  # Clear the terminal screen for updates
#             # Sniff Wi-Fi packets
#             sniff(iface=SELECTED_INTERFACE, prn=process_packet, timeout=2)

#             # Display information about Wi-Fi networks and their clients
#             table_data = []
#             for bssid, info in networks.items():
#                 ssid = info["SSID"]
#                 channel = info["Channel"]
#                 clients = ", ".join(info["Clients"])
#                 table_data.append([ssid, bssid, channel, clients])

#             table_headers = ["SSID", "BSSID", "Channel", "Clients"]
#             print(tabulate(table_data, headers=table_headers, tablefmt="plain"))
#             print("Interface: " + SELECTED_INTERFACE)

#             # Clear the networks data for the next scan
#             networks.clear()

#             # Wait for a few seconds before the next scan
#             time.sleep(2)

#     except KeyboardInterrupt:
#         pass

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     start_scan()

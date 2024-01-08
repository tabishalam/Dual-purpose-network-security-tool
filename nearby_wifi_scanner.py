from tabulate import tabulate
from scapy.all import *
import time
import os

# SSID - Name of the network
# BSSID - MAC address of the network

# Discovered network and their clients
networks = {}


# Extracting BSSID, SSID, channel and client information from network packet
def process_packet(packet):
    if packet.haslayer(Dot11):
        # Checking network and storing them
        if packet.type == 0 and packet.subtype == 8:
            ssid = packet.info.decode("utf-8")  # Decoding bytes to utf-8 / human-readable language
            bssid = packet.addr2
            channel = int(ord(packet[Dot11Elt:3].info))

            if bssid not in networks:
                # networks.append({"SSID": ssid, "Channel": channel})
                networks[bssid] = {"SSID": ssid, "Channel": channel}
                # networks[bssid] = {"SSID": ssid, "Channel": channel, "Clients": set()}


def start_scan():
    try:
        while True:
            # Clear the terminal screen for updates
            os.system("clear")
            # sniff(iface=interface, prn=process_packet, timeout=4)

            print(networks)
            # Display information about Wi-Fi networks and their clients
            data_table = tabulate(networks.items(), headers="keys", tablefmt="plain")
            print(data_table)
    #         print("SSID \t\t\t BSSID \t\t\t Channel")
    #         for bssid, info in networks.items():
    #             ssid = info["SSID"]
    #             channel = info["Channel"]
    #             clients = info["Clients"]
    #             #print(f"SSID: {ssid}, BSSID: {bssid}, Channel: {channel}")
    #             print(f"{ssid} \t\t\t {bssid} \t\t\t {channel}")
    #             #print("Clients:")
    #             #for client_mac in clients:
    #             #   print(f"  - {client_mac}")
    # #
    #         # Clear the networks data for the next scan
    #         #networks = {}
    #
    #         # Wait for a few seconds before the next scan
            time.sleep(2)

    except KeyboardInterrupt:
        pass
from tabulate import tabulate
from threading import Thread
from scapy.all import *
import pandas as pd
import time
import os

# Dictionary to store networks data
networks_data = {}


def sniff_packet(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = str(packet[Dot11].addr2)  # Gets the MAC address of the network
        ssid = str(packet[Dot11Elt].info.decode())  # Gets the name of the network

        # Get signal strength
        try:
            signal = packet.dBm_AntSignal
        except:
            signal = "N/A"

        stats = packet[Dot11Beacon].network_stats()  # Extract network stats
        channel = stats.get("channel")  # Get the channel of the network
        encryption = list(stats.get("crypto"))[0]  # Get encryption type

        data = {"bssid": bssid, "ssid": ssid, "signal": signal, "channel": channel, "encryption": encryption}

        # Add data to the dictionary
        networks_data[bssid] = data


# Displays the networks
def display_networks():
    while True:
        os.system("clear")  # Clear the terminal
        df = pd.DataFrame(list(networks_data.values()))
        df.index.name = "WiFi No."
        print(df.to_markdown(index=True))
        time.sleep(0.5)


# Change channel every 0.5 sec to find networks broadcasting on different channels
def change_channel():
    # ch_2_4ghz = 1
    # ch_5ghz = 36  # Starting channel for 5 GHz
    
    ch_2_4ghz = 1
    ch_5ghz = 36

    while True:
        os.system(f"iwconfig {interface} channel {ch_2_4ghz}")
        time.sleep(0.5)
        os.system(f"iwconfig {interface} channel {ch_5ghz}")
        ch = ch_2_4ghz % 14 + 1
        ch = ch_5ghz % 165 + 1
        time.sleep(0.5)

    # while True:
    #     i = 0
    #     j = 36

    #     while i < 14:
    #         # Set channels in the 2.4 GHz range
    #         os.system(f"iwconfig {interface} channel {ch_2_4ghz}")
    #         ch_2_4ghz = (ch_2_4ghz % 14) + 1  # Switch to the next channel in the 2.4 GHz range
    #         print(ch_2_4ghz)
    #         time.sleep(0.5)
    #         i += 1

    #     while j < 165:
    #         # Set channels in the 5 GHz range
    #         os.system(f"iwconfig {interface} channel {ch_5ghz}")
    #         ch_5ghz = (ch_5ghz % 165) + 1  # Switch to the next channel in the 5 GHz range
    #         print(ch_5ghz)
    #         time.sleep(0.5)
    #         j += 1


if __name__ == "__main__":
    interface = "wlan0"
    printer = Thread(target=display_networks)
    printer.daemon = True
    printer.start()

    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    sniff(prn=sniff_packet, iface=interface)

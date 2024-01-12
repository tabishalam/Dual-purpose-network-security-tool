from threading import Thread
from scapy.all import *
import pandas
import time
import os



# Dataframe to contain all the nearby WiFi networks
networks_list = pandas.DataFrame(columns=["BSSID", "SSID", "Signal", "Channel", "Encryption"])
# Sets the index to MAC address of the network
networks_list.set_index("BSSID", inplace=True)


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2 # Gets the mac address of network
        ssid = packet[Dot11Elt].info.decode() # Gets the name of network

        # Get signal strength
        try:
            signal = packet.dBm_AntSignal
        except:
            signal = "N/A"

        # Extract network stats
        stats = packet[Dot11Beacon].network_stats()

        # Get channel of the network
        channel = stats.get("channel")

        # Get encryption type
        encryption = stats.get("crypto")
        networks_list.loc[bssid] = (ssid, signal, channel, encryption)


def display_networks():
    while True:
        os.system("clear")
        print(networks_list)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 14 + 1
        time.sleep(0.5)


if __name__ == "__main__":
    Interface = "wlan0"
    printer = Thread(target=display_networks)
    printer.daemon = True
    printer.start()

    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    sniff(prn=callback, iface=Interface)


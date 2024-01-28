import os
import time
import pandas as pd
from scapy.all import *
from threading import Thread


# Dictionary to store networks data
SCANNED_NETWORKS = {}

# Global flag to signal threads to stop
STOP_THREADS = False


# Select a network from the scanned network list
def select_network():
    selected_wifi = int(input("\n Select any WiFi network: "))
    
    networks =  pd.DataFrame(list(SCANNED_NETWORKS.values()))
    networks_id =  list(SCANNED_NETWORKS)

    selected_network = networks_id[selected_wifi] 
    print(networks.get(selected_network))   


def sniff_packet(packet):
    global STOP_THREADS

    if STOP_THREADS:
        return

    if packet.haslayer(Dot11Beacon):
        bssid = str(packet[Dot11].addr2)  # Gets the MAC address of the network
        ssid = str(packet[Dot11Elt].info.decode())  # Gets the name of the network

        # Get signal strength
        signal = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else -100

        stats = packet[Dot11Beacon].network_stats()  # Extract network stats
        channel = stats.get("channel")  # Get the channel of the network
        encryption = list(stats.get("crypto"))[0] if stats.get("crypto") else "N/A"  # Get encryption type

        data = {"bssid": bssid, "ssid": ssid, "signal": signal, "channel": channel, "encryption": encryption}

        # Add data to the dictionary
        SCANNED_NETWORKS[bssid] = data


# Print scanned wifi networks
def print_final_scan():
    df = pd.DataFrame(list(SCANNED_NETWORKS.values()))
    df.index.name = "WiFi No."
    print(df.to_markdown(index=True))
    time.sleep(1)    


# Displays the networks
def print_networks():
    global STOP_THREADS

    while not STOP_THREADS:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal
        df = pd.DataFrame(list(SCANNED_NETWORKS.values()))
        df.index.name = "WiFi No."
        print(df.to_markdown(index=True))
        time.sleep(0.5)


# Change channel every 0.5 sec to find networks broadcasting on different channels
def change_channel(interface):
    global STOP_THREADS

    ch_2_4ghz = 1
    ch_5ghz = 36

    while not STOP_THREADS:
        os.system(f"iwconfig {interface} channel {ch_2_4ghz}")
        time.sleep(0.1)
        ch_2_4ghz = (ch_2_4ghz % 14) + 1
        time.sleep(0.1)
        
        os.system(f"iwconfig {interface} channel {ch_5ghz}")
        ch_5ghz = (ch_5ghz % 165) + 1
        time.sleep(0.5)

        print(interface)
        print("4G: ", ch_2_4ghz)
        print("5G: ", ch_5ghz)
        print(STOP_THREADS)
        
        if ch_5ghz == 165:
            ch_5ghz = 36


# Starts wifi scanning
def start_scan(SELECTED_INTERFACE):
    global STOP_THREADS

    printer = Thread(target=print_networks)
    printer.daemon = True
    printer.start()

    channel_changer = Thread(target=change_channel, args=(SELECTED_INTERFACE,))
    channel_changer.daemon = True
    channel_changer.start()

    try:
        sniff(prn=sniff_packet, iface=SELECTED_INTERFACE)

    except KeyboardInterrupt:
        pass

    finally:
        STOP_THREADS = True
        print("Scanning Complete...")
        printer.join()  # Wait for the printer thread to finish
        channel_changer.join()  # Wait for the channel_changer thread to finish


if __name__ == "__main__":
    interface = "wlan0"
    printer = Thread(target=print_networks)
    printer.daemon = True
    printer.start()

    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    try:
        sniff(prn=sniff_packet, iface=interface)
    except KeyboardInterrupt:
        STOP_THREADS = True

    finally:
        time.sleep(2)  # Allow threads to finish
        print("Scanning Complete...")

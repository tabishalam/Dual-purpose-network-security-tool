# 192.168.170.2
import scapy.all as scapy
import subprocess


# Print connected devices
def print_clients(result):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    for client in result:
        print(client["ip"]+ "\t\t" + client["mac"])


# Fetch all the connected devices on the network
def scan(gateway_ip):
    ip_range = gateway_ip + "/24"
    print(ip_range)
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for client in answered_list:
        client_dict = {"ip": client[1].psrc, "mac": client[1].hwsrc}
        clients_list.append(client_dict)

    print_clients(clients_list)


# Gets the default gateway ip address or ip address of router
def default_gateway(selected_interface):
    command = f"ip route show dev {selected_interface}"
    output = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    
    gateway_ip = output.stdout.split()[2]

    return gateway_ip

    # if len(gateway_ip) > 0:
    # else:
    #     print("Connect to a router to get gateway ip address.")


# Starts scanning
def start_scan(selected_interface):
    gateway_ip = default_gateway(selected_interface)
    scan(gateway_ip)

if __name__ == "__main__":
    gateway_ip = input("Enter ip address of the gateway: ")
    scan(gateway_ip)
    
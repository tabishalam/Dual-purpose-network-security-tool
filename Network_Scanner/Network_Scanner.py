import scapy.all as scapy
import subprocess


# Print connected devices
def display_clients(result):
    print("IP\t\t\tMAC Address\n-------------------------------------")
    
    for client in result:
        print(client["ip"]+ "\t\t" + client["mac"])


# Fetch all the connected devices on the network
def scan_devices(gateway_ip):
    ip_range = gateway_ip + "/24"
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for client in answered_list:
        client_dict = {"ip": client[1].psrc, "mac": client[1].hwsrc}
        clients_list.append(client_dict)

    display_clients(clients_list)


# Gets the default gateway ip address or ip address of router
def default_gateway(SELECTED_INTERFACE):
    try:
        command = f"sudo ip route show dev {SELECTED_INTERFACE}"
        output = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        gateway_ip = output.stdout.split()[2]

        return gateway_ip
    
    except Exception as e:
        print(e)


# Starts scanning
def start_scan(SELECTED_INTERFACE):
    gateway_ip = default_gateway(SELECTED_INTERFACE)
    scan_devices(gateway_ip)


if __name__ == "__main__":
    print("Note: Make sure you are connected to the same network before running the program...")
    gateway_ip = input("Enter ip address of the gateway: ")
    scan_devices(gateway_ip)
    
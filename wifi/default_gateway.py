import subprocess


def default_gateway(selected_interface):
    command = f"ip route show dev {selected_interface}"
    output = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

    gateway_ip = output.stdout.split()[2]
    
    if len(gateway_ip) > 0:
        return gateway_ip
    else:
        print("Connect to a router to get gateway ip address.")

if __name__ == "__main__":
    scan("wlan0")
import subprocess


def scan(selected_interface):
    command = f"ip route show dev {selected_interface}"
    output = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

    print(output.stdout.split()[2])


if __name__ == "__main__":
    scan("wlan0")
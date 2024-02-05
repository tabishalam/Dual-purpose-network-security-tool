import time
import sys
import subprocess
import re

def run_airodump(interface, bssid, channel):
    command = ["sudo", "airodump-ng", "--bssid", bssid, "--channel", str(channel), interface]

    clients_dict = {}
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

        # # Read and print the output in real-time
        # while True:
        #     output = process.stdout.readline()
        #     if output == '' and process.poll() is not None:
        #         break
        #     if output:
        #         print(output)
        #         # sys.stdout.flush()  # Add this line

        # Skip the header lines for Access Point details
        for _ in range(6):
            process.stdout.readline()

        # Read and parse client details
        # while True:
        #     output = process.stdout.readline()
        #     if output.startswith("Station"):
        #         break
            
        while True:
            subprocess.run("clear")
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            print(output)
            if output.strip():
                # Extract relevant information using regex
                match = re.match(r'^([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+)$', output.strip())
                print(match)
                if match:
                    client_bssid, first_seen, last_seen, power, packets, bssid, probed_essids, _, _ = match.groups()
                    print(client_bssid)
                    clients_dict[client_bssid] = {
                        'first_seen': first_seen,
                        'last_seen': last_seen,
                        'power': power,
                        'packets': packets,
                        'associated_bssid': bssid,
                        'probed_essids': probed_essids,
                    }

                time.sleep(2)

        process.communicate()  # Wait for the process

        return clients_dict

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None
    
    except KeyboardInterrupt:
        print(clients_dict)
    except subprocess.TimeoutExpired:
        print("The command timed out after 10 seconds.")
        return None

# Example usage
interface_card = 'wlan0'
target_bssid = 'C4:71:54:56:CA:6B'
channel_no = 11

clients_info = run_airodump(interface_card, target_bssid, channel_no)
if clients_info:
    print(clients_info)

import subprocess

def get_connected_interface():
    try:
        result = subprocess.run(['ip', '-br', 'link', 'show'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.split('\n')

        for line in output_lines:
            parts = line.split(",")
            print(parts)
            if len(parts) >= 3 and parts[2] == 'UP':
                return parts[0]

        return None  # No connected interface found

    except subprocess.CalledProcessError:
        print("Error executing 'ip -br link show' command.")

# Get the currently connected network interface
connected_interface = get_connected_interface()

if connected_interface:
    print(f"The connected network interface is: {connected_interface}")
else:
    print("No network interface is currently connected.")
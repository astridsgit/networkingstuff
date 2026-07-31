import subprocess
import socket

subnet = "192.168.1." # Remember to use your actual subnet!

print("Starting upgraded network sweep...")

for i in range(1, 51):
    ip_address = subnet + str(i)

    # 1. Ping the device to wake it up and force it to share its MAC address
    response = subprocess.call(
        ['ping', '-c', '1', '-W', '1', ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # If the device responds (response == 0), we gather more info
    if response == 0:
        mac_address = "Unknown MAC"
        hostname = "Unknown Name"

        # --- GETTING THE HOSTNAME ---
        try:
            # socket.gethostbyaddr asks the network for the device's name
            # It returns a tuple, and the name is the first item [0]
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            # If the device refuses to share a name, we just catch the error and move on
            pass

        # --- GETTING THE MAC ADDRESS ---
        # We run 'ip neigh show <ip>' to check our local ARP table
        # capture_output=True grabs the text so we can read it in Python
        arp_result = subprocess.run(
            ['ip', 'neigh', 'show', ip_address],
            capture_output=True,
            text=True
        )

        # The output looks like: "192.168.1.5 dev wlan0 lladdr aa:bb:cc:dd:ee:ff REACHABLE"
        # We split the sentence into a list of words to find the MAC address easily
        output_words = arp_result.stdout.split()

        if 'lladdr' in output_words:
            # The MAC address is always the word immediately after 'lladdr'
            mac_index = output_words.index('lladdr') + 1
            mac_address = output_words[mac_index]

        print(f"[+] IP: {ip_address} | Name: {hostname} | MAC: {mac_address}")

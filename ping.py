import subprocess
import socket

subnet = "192.168.1."

print("Starting upgraded network sweep...")


for i in range(1, 51):
    ip_address = subnet + str(i)
    response = subprocess.call(
        ['ping', '-c', '1', '-W', '1', ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if response == 0:
        mac_address = "Unknown MAC"
        hostname = "Unknown Name"
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            pass

        arp_result = subprocess.run(
            ['ip', 'neigh', 'show', ip_address],
            capture_output=True,
            text=True
        )
        output_words = arp_result.stdout.split()
        if 'lladdr' in output_words:
            mac_index = output_words.index('lladdr') + 1
            mac_address = output_words[mac_index]
        print(f"[+] IP: {ip_address} | Name: {hostname} | MAC: {mac_address}")

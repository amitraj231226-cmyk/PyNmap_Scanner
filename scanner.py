import nmap
import os
from datetime import datetime

banner = r"""
███╗   ██╗███████╗████████╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗     ██║   ██████╔╝██████╔╝██║   ██║██████╔╝█████╗
██║╚██╗██║██╔══╝     ██║   ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝
██║ ╚████║███████╗   ██║   ██║     ██║  ██║╚██████╔╝██████╔╝███████╗
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

              Network Reconnaissance & Port Scanner
                     Version 2.0 | Built in Python
                     Created by Ajit Raj
"""

scanner = nmap.PortScanner()

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

print(BLUE + "=" * 50)
print("         NETPROBE ADVANCED SCANNER")
print("=" * 50 + RESET)
print("\033[92m" + banner + "\033[0m")

target = input("Enter target IP/domain: ")
port_range = input("Enter port range (example 1-1000): ")

print("\nScan Types:")
print("1. Quick Scan")
print("2. Service Detection")
print("3. Aggressive Scan")

choice = input("Choose scan type: ")

if choice == "1":
    arguments = "-T4"
elif choice == "2":
    arguments = "-sV"
elif choice == "3":
    arguments = "-A"
else:
    print(RED + "Invalid choice. Defaulting to Service Detection." + RESET)
    arguments = "-sV"

print(YELLOW + f"\nScanning {target}...\n" + RESET)

try:
    scanner.scan(target, port_range, arguments=arguments)

    report = []

    for host in scanner.all_hosts():
        print(GREEN + "=" * 50)
        print(f"Host: {host}")
        print(f"State: {scanner[host].state()}" + RESET)

        report.append(f"Host: {host}")
        report.append(f"State: {scanner[host].state()}")

        for proto in scanner[host].all_protocols():
            print(BLUE + f"\nProtocol: {proto}" + RESET)

            ports = sorted(scanner[host][proto].keys())

            for port in ports:
                state = scanner[host][proto][port]['state']
                service = scanner[host][proto][port]['name']

                output = f"Port: {port} | State: {state} | Service: {service}"

                if state == "open":
                    print(GREEN + output + RESET)
                else:
                    print(RED + output + RESET)

                report.append(output)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write("\n".join(report))

    print(YELLOW + f"\nReport saved: {filename}" + RESET)

except Exception as e:
    print(RED + f"Error: {e}" + RESET)
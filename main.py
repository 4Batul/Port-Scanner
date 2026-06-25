import socket
import sys  
from concurrent.futures import ThreadPoolExecutor
import csv

port_dict = {}
with open('ports.csv', mode='r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    for row in reader:
        port = int(row[1])
        description = row[2]
        port_dict[port] = description

bannerTxt = """                                
  _____ ____ ____    ____            _     ____                                  
 |_   _/ ___|  _ \  |  _ \ ___  _ __| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
   | || |   | |_) | | |_) / _ \| '__| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
   | || |___|  __/  |  __/ (_) | |  | |_   ___) | (__\__,_|_| |_|_| |_|\___|_| | | 
 ********************************************************************************  
    Github: 4Batul
    Linkedin: Arhama Batool
    """
print(bannerTxt)
print("Multi-Threaded TCP Port Scanner")
ports_open = 0
stack = []  
target = input("Enter the target (e.g., 127.0.0.1 or scanme.nmap.org): ")
choice = int(input("1.For a range of ports eg, 130-2000 \n2. For custom multiple inputs eg,23,45,135,139\n"))
if choice == 1:
    port_start = int(input("Starting port: "))
    port_end = int(input("Ending Port: "))
    ports_to_scan = range(port_start, port_end + 1)

else:
    def get_port_input(prompt):
        max_ports = 100
        while True:
            try:
                ports_input = input(prompt)
            # Expecting comma-separated ports, e.g., 80,443,8080
                ports_list = [int(p.strip()) for p in ports_input.split(',')]
                if len(ports_list) > max_ports:
                    print(f"Please enter no more than {max_ports} ports.")
                else:
                    return ports_list
            except ValueError:
                print("Invalid input. Please enter comma-separated port numbers.")
    ports_to_scan = get_port_input("Enter ports (comma-separated, e.g., 80,443,8080): ")


MAX_THREADS = 100 

def scan_port(port):
    """Scans a single port and attempts to grab its service banner."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) 
        result = s.connect_ex((target, port))
        if result == 0:
            banner = "Unknown Service (No banner returned)"
            try:
                s.sendall(b"Hello\r\n") 
                data = s.recv(1024)
                if data:
                    # Decode the bytes into readable text, stripping messy whitespace
                    banner = data.decode('utf-8', errors='ignore').strip()
            except Exception:
                pass
            print(f"[*] Port {port} is OPEN -> Banner: {banner}")
            s.close()
            return port, banner
        s.close()
    except Exception:
        pass
    return None

print(f"\nScanning {target} using {MAX_THREADS} simultaneous threads...\n")
open_ports = []

try:
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # map() passes each port from our range into the scan_port function
        results = executor.map(scan_port, ports_to_scan)
        for res in results:
            if res:
                open_ports.append(res)
except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user. Exiting...")
    sys.exit()

print("\n--- Scan Summary ---")
print(f"Total open ports found: {len(open_ports)}")
for port, banner in open_ports:
    description = port_dict.get(port, "No description available")
    print(f"Port {port}: {description}")

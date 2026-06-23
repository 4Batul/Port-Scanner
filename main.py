import socket
import sys  
from concurrent.futures import ThreadPoolExecutor

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
port_start = int(input("Starting port: "))
port_end = int(input("Ending Port: "))
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
        ports_to_scan = range(port_start, port_end + 1)
        results = executor.map(scan_port, ports_to_scan)
        for res in results:
            if res:
                open_ports.append(res)
except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user. Exiting...")
    sys.exit()

print("\n--- Scan Summary ---")
print(f"Total open ports found: {len(open_ports)}")




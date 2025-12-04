import socket
import  csv

def scanPort(host, port, openPorts):
    """
    Try to connect to a specified host and port.
    If successful, record and print the port and any banner.
    """ 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        # connect to our target port
        sock.connect((host, port)) 
        print(f"[+] Port {port} is open")
        banner = ""
        try:
            # Attempt to read banner (servaice may say welcom message)
            banner = sock.recv(1024).decode().strip()
            if banner:
                print(f"    Banner: {banner}")
        except Exception:
            pass
        sock.close()
        # Record the open port and banner for later saving
        openPorts.append((port, banner))
    except Exception:
        pass

def main():
    host = input("Enter target IP or hostname: ").strip()
    portRange = input("Enter port range (e.g 20-1024): ").strip()
    if '-' in portRange:
        startPort, endPort = portRange.split('-')
        startPort, endPort = int(startPort), int(endPort)
    else:
        startPort = endPort = int(portRange)# Single port scan
    print(f"Scanning {host} from port {startPort} to {endPort}...")
    openPorts = []
    for port in range(startPort, endPort + 1):
        scanPort(host, port, openPorts)
    # Save results to CSV
    if openPorts:
        with open('scanResults.csv','w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Port', 'Banner'])
            for port, banner in openPorts:
                writer.writerow([port, banner])
        print("Scan results saved to scanResults.csv")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
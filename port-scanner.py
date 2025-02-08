import socket
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import signal
import sys
from datetime import datetime
from tqdm import tqdm

# ANSI color codes
class Colors:
    """
    Class for ANSI color codes. 
    Inspired by: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Global flag for graceful shutdown
stop_scan = False
# Global progress bar
progress_bar = None

def signal_handler(signum, frame):
    """Handle Ctrl+C by setting the stop flag and printing a message"""
    global stop_scan, progress_bar
    print(f"\n{Colors.YELLOW}[!] Ctrl+C detected. Shutting down gracefully...{Colors.ENDC}")
    stop_scan = True
    if progress_bar:
        progress_bar.close()

def print_banner(target, start_port, end_port):
    """Print a styled banner for the scan"""
    banner = f"""
{Colors.BOLD}{Colors.BLUE}╔══════════════════════════════════════════════════════════╗
║                    PORT SCANNER v1.0                     ║
║                Created by: SHABARI_K_S                   ║
╚══════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.GREEN}[*] Target Host:{Colors.ENDC} {target}
{Colors.GREEN}[*] Port Range:{Colors.ENDC} {start_port}-{end_port}
{Colors.GREEN}[*] Scan started at:{Colors.ENDC} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{Colors.BLUE}{"=" * 60}{Colors.ENDC}

"""  # Added extra newline for spacing
    print(banner)

def scan_port(target, port, timeout):
    """
    Scan a single port on the target host.
    Returns tuple of (port, status, service_name if available)
    """
    global progress_bar
    
    if stop_scan:
        return (port, False, None)
        
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            return (port, True, service)
        return (port, False, None)
    
    except socket.gaierror:
        print(f"{Colors.RED}[!] Hostname could not be resolved{Colors.ENDC}")
        return (port, False, None)
    except socket.error:
        print(f"{Colors.RED}[!] Could not connect to server{Colors.ENDC}")
        return (port, False, None)
    finally:
        sock.close()
        if progress_bar:
            progress_bar.update(1)

def main():
    global progress_bar
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description=f'{Colors.BOLD}Simple Port Scanner with Progress Bar{Colors.ENDC}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('target', help='Target host to scan')
    parser.add_argument('-p', '--ports', help='Port range to scan (e.g., 20-100)', default='1-1024')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use', default=50)
    parser.add_argument('--timeout', type=float, help='Timeout for each port scan in seconds', default=1.0)
    
    args = parser.parse_args()
    
    # Parse port range
    start_port, end_port = map(int, args.ports.split('-'))
    ports = range(start_port, end_port + 1)
    total_ports = len(ports)
    
    print_banner(args.target, start_port, end_port)
    
    start_time = time.time()
    results = []
    
    try:
        # Print initial space before progress bar
        print(f"{Colors.BLUE}[*] Starting scan...{Colors.ENDC}\n")
        
        # Initialize progress bar
        progress_bar = tqdm(
            total=total_ports,
            desc=f"{Colors.BLUE}Scanning{Colors.ENDC}",
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} ports [{elapsed}<{remaining}]',
            leave=False  # Don't leave the progress bar after completion
        )
        
        # Use ThreadPoolExecutor for concurrent scanning
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [executor.submit(scan_port, args.target, port, args.timeout) for port in ports]
            
            # Collect results as they complete
            for future in futures:
                if stop_scan:
                    executor.shutdown(wait=False)
                    break
                try:
                    result = future.result()
                    if result[1]:  # If port is open
                        results.append(result)
                        # Move to new line to avoid interfering with progress bar
                        tqdm.write(f"{Colors.GREEN}[+] Port {result[0]} is open ({result[2]}){Colors.ENDC}")
                except Exception as e:
                    tqdm.write(f"{Colors.RED}[!] Error processing result: {e}{Colors.ENDC}")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.ENDC}")
    finally:
        if progress_bar:
            progress_bar.close()
        
        scan_duration = time.time() - start_time
        
        # Print extra newline for spacing after progress bar
        print("\n")
        
        # Print final results
        print(f"{Colors.BOLD}{Colors.BLUE}Scan Results:{Colors.ENDC}")
        print(f"{Colors.BLUE}{'-' * 60}{Colors.ENDC}")
        if results:
            print(f"{Colors.BOLD}{'PORT':<10}{'STATE':<10}{'SERVICE'}{Colors.ENDC}")
            for port, _, service in sorted(results):
                print(f"{Colors.GREEN}{port:<10}{'open':<10}{service}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}No open ports found{Colors.ENDC}")
        
        print(f"\n{Colors.BLUE}[*] Scan completed in {scan_duration:.2f} seconds{Colors.ENDC}")
        
        if stop_scan:
            print(f"{Colors.YELLOW}[!] Scan was interrupted before completion{Colors.ENDC}")
            sys.exit(1)

if __name__ == "__main__":
    main()

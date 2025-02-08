# Python Port Scanner

A feature-rich, multi-threaded port scanner with a colorful interface and real-time progress tracking.

## Features

- 🚀 Multi-threaded scanning for fast results
- 📊 Real-time progress bar
- 🎨 Colored output for better visibility
- 🎯 Customizable port ranges
- ⚡ Service detection for open ports
- 🛑 Graceful handling of Ctrl+C interruption
- ⚙️ Configurable thread count and timeout settings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner
```

2. Install required dependencies:
```bash
pip install tqdm
```

## Usage

Basic usage:
```bash
python port_scanner.py example.com
```

Advanced usage with options:
```bash
python port_scanner.py example.com -p 20-1000 -t 100 --timeout 0.5
```

### Command Line Arguments

- `target`: Target host to scan (required)
- `-p, --ports`: Port range to scan (default: 1-1024)
- `-t, --threads`: Number of threads to use (default: 50)
- `--timeout`: Timeout for each port scan in seconds (default: 1.0)

### Example Output

```
╔══════════════════════════════════════════════════════════╗
║                     PORT SCANNER                         ║
║                Created by: SHABARI_K_S                   ║
╚══════════════════════════════════════════════════════════╝

[*] Target Host: example.com
[*] Port Range: 1-1024
[*] Scan started at: 2024-02-08 10:30:15
============================================================

[*] Starting scan...


[+] Port 80 is open (http)
[+] Port 443 is open (https)

Scanning: |██████████████████████| 1024/1024 ports [00:31<00:00]

Scan Results:
------------------------------------------------------------
PORT      STATE     SERVICE
80        open      http
443       open      https

[*] Scan completed in 31.24 seconds
```

## Features Explained

### Multi-threading
The scanner uses Python's ThreadPoolExecutor to scan multiple ports simultaneously, significantly reducing scan time.

### Progress Tracking
- Real-time progress bar showing:
  - Number of ports scanned
  - Percentage complete
  - Estimated time remaining
  - Elapsed time

### Color Coding
- Green: Open ports and success messages
- Red: Errors and warnings
- Blue: Headers and status messages
- Yellow: Warnings and interruption messages

### Service Detection
Automatically identifies and displays common services running on open ports.

## Security Notice

⚠️ Only use this tool on systems you have permission to scan. Unauthorized port scanning may be illegal in some contexts.

## Error Handling

The scanner handles various network-related errors:
- Host resolution failures
- Connection timeouts
- Connection refused
- Ctrl+C interruption

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses `tqdm` library for progress bar functionality
- Inspired by classic network scanning tools
- Thanks to all contributors and testers

## Support

For support, please open an issue in the GitHub repository.

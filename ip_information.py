
import socket
import urllib.request
import subprocess

print("=" * 50)
print("       PYTHON CYBERSECURITY TOOLKIT")
print("          IP INFORMATION TOOL")
print("=" * 50)

# 1. Get Computer Hostname
hostname = socket.gethostname()

# 2. Get Local IP Address
try:
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.connect(("1.1.1.1", 80))
    local_ip = connection.getsockname()[0]
    connection.close()
except OSError:
    local_ip = socket.gethostbyname(hostname)

# 3. Get Public IP Address
try:
    url = "https://api.ipify.org"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Python-Cybersecurity-Toolkit"}
    )

    with urllib.request.urlopen(request, timeout=5) as response:
        public_ip = response.read().decode("utf-8")

except Exception:
    public_ip = "Unable to retrieve Public IP"

# 4. Check Internet Connection
try:
    test = socket.create_connection(("1.1.1.1", 53), timeout=3)
    internet_status = "Connected"
    test.close()
except OSError:
    internet_status = "Not Connected / Blocked"

# 5. Display Basic Information
print("\n[+] COMPUTER INFORMATION")
print("-" * 50)
print("Hostname       :", hostname)
print("Local IP       :", local_ip)
print("Public IP      :", public_ip)
print("Internet Status:", internet_status)

# 6. Display Windows Network Configuration
print("\n[+] NETWORK CONFIGURATION")
print("-" * 50)

try:
    result = subprocess.run(
        ["ipconfig", "/all"],
        capture_output=True,
        text=True,
        errors="replace"
    )

    print(result.stdout)

except Exception as error:
    print("Network information error:", error)

print("\n[+] INFORMATION COLLECTION COMPLETED!")
print("=" * 50)

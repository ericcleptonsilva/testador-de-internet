import subprocess
import socket
import requests
import speedtest
import platform
import re

def check_internet_connection(host="8.8.8.8"):
    """
    Checks internet connection by pinging a reliable host.
    Returns True if connected, False otherwise.
    """
    return ping_host(host) is not None

def get_ip_info():
    """
    Retrieves local and public IP addresses.
    Returns a dictionary with 'local_ip' and 'public_ip'.
    """
    # Get Local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    # Get Public IP
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        public_ip = response.json().get('ip')
    except Exception:
        public_ip = "Unavailable"

    return {
        "local_ip": local_ip,
        "public_ip": public_ip
    }

def run_speed_test():
    """
    Runs a speed test using speedtest-cli.
    Returns a dictionary with 'download', 'upload', 'ping', 'server'.
    Download/Upload in Mbps.
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = st.results.ping
        server = st.results.server

        return {
            "download": round(download_speed, 2),
            "upload": round(upload_speed, 2),
            "ping": ping,
            "server": f"{server['sponsor']} ({server['name']})",
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def ping_host(host):
    """
    Pings a specific host.
    Returns latency in ms if successful, None otherwise.
    """
    # Windows uses -n, others use -c
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    try:
        # Run ping command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            # Parse output for time.
            # Windows: "time=12ms"
            # Linux: "time=12.3 ms"
            output = result.stdout

            # Regex to find time=...
            # Works for Windows and Linux usually
            match = re.search(r'time[=<]([\d\.]+)\s?ms', output, re.IGNORECASE)
            if match:
                return float(match.group(1))
            return 0.0 # Connected but couldn't parse time
        else:
            return None
    except Exception:
        return None

def ping_host_multiple(host, count=5):
    """
    Pings a host multiple times.
    Returns a list of latencies (in ms).
    """
    latencies = []
    for _ in range(count):
        latency = ping_host(host)
        if latency is not None:
            latencies.append(latency)
        else:
            latencies.append(0.0) # 0.0 indicates timeout/failure
    return latencies

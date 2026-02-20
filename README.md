# Network Diagnostic Tool

A cross-platform network diagnostic tool written in Python. It runs on Windows, Linux, and Android (via Termux).

## Features

-   **Connectivity Check:** Quick ping to a reliable host (Google DNS).
-   **IP Information:** Displays local and public IP addresses.
-   **Speed Test:** Measures download and upload speeds using `speedtest-cli`.
-   **Ping Utility:** Measure latency to any specific host.
-   **Cross-Platform:** Designed to work on Windows, Linux, and Android.

## Prerequisites

-   Python 3.x
-   pip (Python package manager)

## Installation

1.  Clone the repository or download the source code.
2.  Navigate to the project root directory.
3.  Install dependencies:
    ```bash
    pip install -r network_diagnostic_tool/requirements.txt
    ```

## Usage

### Run the Tool

Run the main script using Python from the root directory:

```bash
python -m network_diagnostic_tool.main
```

### Menu Options

1.  **Full Diagnostic:** Runs all checks in sequence (Connectivity, IP, Speed Test).
2.  **Quick Connectivity Check:** Checks internet access and displays IP info.
3.  **Speed Test Only:** Runs a speed test (Download/Upload/Ping).
4.  **Ping Specific Host:** Allows you to enter a hostname or IP to ping.
5.  **Exit:** Closes the application.

## Android (Termux) Instructions

1.  Install [Termux](https://termux.com/) from F-Droid or Google Play.
2.  Update packages:
    ```bash
    pkg update && pkg upgrade
    ```
3.  Install Python and Git:
    ```bash
    pkg install python git
    ```
4.  Clone this repository (or copy the files).
5.  Install dependencies:
    ```bash
    pip install -r network_diagnostic_tool/requirements.txt
    ```
6.  Run the tool:
    ```bash
    python -m network_diagnostic_tool.main
    ```

## Troubleshooting

-   **Permission Denied (Ping):** On some Linux systems, `ping` might require root privileges. However, this tool uses the system `ping` command via `subprocess`, which usually works for standard users.
-   **Speed Test Failed:** If the speed test fails, check your internet connection. Sometimes `speedtest-cli` servers are busy.

## License

MIT

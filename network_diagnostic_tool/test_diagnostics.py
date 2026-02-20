import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the package can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network_diagnostic_tool.diagnostics import check_internet_connection, get_ip_info, run_speed_test, ping_host

class TestDiagnostics(unittest.TestCase):

    @patch('network_diagnostic_tool.diagnostics.ping_host')
    def test_check_internet_connection(self, mock_ping):
        # Test Connected
        mock_ping.return_value = 12.5
        self.assertTrue(check_internet_connection())

        # Test Disconnected
        mock_ping.return_value = None
        self.assertFalse(check_internet_connection())

    @patch('network_diagnostic_tool.diagnostics.socket')
    @patch('network_diagnostic_tool.diagnostics.requests.get')
    def test_get_ip_info(self, mock_get, mock_socket):
        # Mock Local IP
        mock_sock_instance = MagicMock()
        mock_socket.socket.return_value = mock_sock_instance
        mock_sock_instance.getsockname.return_value = ['192.168.1.10']

        # Mock Public IP
        mock_response = MagicMock()
        mock_response.json.return_value = {'ip': '203.0.113.1'}
        mock_get.return_value = mock_response

        info = get_ip_info()
        self.assertEqual(info['local_ip'], '192.168.1.10')
        self.assertEqual(info['public_ip'], '203.0.113.1')

    @patch('network_diagnostic_tool.diagnostics.speedtest.Speedtest')
    def test_run_speed_test_success(self, mock_speedtest):
        # Mock Speedtest instance
        st_instance = MagicMock()
        mock_speedtest.return_value = st_instance

        st_instance.download.return_value = 50_000_000 # 50 Mbps
        st_instance.upload.return_value = 10_000_000   # 10 Mbps
        st_instance.results.ping = 15.0
        st_instance.results.server = {'sponsor': 'ISP', 'name': 'City'}

        result = run_speed_test()

        self.assertTrue(result['success'])
        self.assertEqual(result['download'], 50.0)
        self.assertEqual(result['upload'], 10.0)
        self.assertEqual(result['ping'], 15.0)
        self.assertIn('ISP', result['server'])

    @patch('network_diagnostic_tool.diagnostics.speedtest.Speedtest')
    def test_run_speed_test_failure(self, mock_speedtest):
        mock_speedtest.side_effect = Exception("Speedtest error")

        result = run_speed_test()
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Speedtest error")

    @patch('network_diagnostic_tool.diagnostics.subprocess.run')
    def test_ping_host_success(self, mock_run):
        # Mock successful ping
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Reply from 8.8.8.8: bytes=32 time=20ms TTL=118"
        mock_run.return_value = mock_result

        latency = ping_host("8.8.8.8")
        self.assertEqual(latency, 20.0)

    @patch('network_diagnostic_tool.diagnostics.subprocess.run')
    def test_ping_host_failure(self, mock_run):
        # Mock failed ping
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        latency = ping_host("invalid.host")
        self.assertIsNone(latency)

if __name__ == '__main__':
    unittest.main()

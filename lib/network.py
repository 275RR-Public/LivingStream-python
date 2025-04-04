import socket
import json

class Network:
    def __init__(self, udp_ip="127.0.0.1", udp_port=5005):
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_ip = udp_ip            # Loopback to Unity's IP (change if needed)
        self.udp_port = udp_port        # Unity's receiving port

    def send_tracking_data(self, tracking_data):
        # Send data to Unity over UDP
        # No filtering; Unity will ignore the 'bbox' field in tracking_data
        udp_message = json.dumps(tracking_data)
        try:
            self.udp_sock.sendto(udp_message.encode("utf-8"), (self.udp_ip, self.udp_port))
            print(f"Sent UDP data: {udp_message}")
        except Exception as e:
            print(f"UDP send error: {e}")

    def close(self):
        self.udp_sock.close()
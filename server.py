from mcp.server.mcpserver import MCPServer
import requests
import os

mcp = MCPServer("ESP32-Hardware-Controller")

ESP32_IP = os.getenv("ESP32_IP", "172.20.10.3")
AUTH_TOKEN = os.getenv("DEVICE_SECRET", "workshop-secret-2026")

@mcp.tool()
def control_led(state: str, duration_ms: int = 0) -> str:
    """Controls the ESP32 LED. state must be 'on' or 'off'. duration_ms pulses the LED for that duration."""
    url = f"http://{ESP32_IP}/led"
    headers = {"X-Device-Auth": AUTH_TOKEN}
    payload = {"state": state.lower(), "duration_ms": duration_ms}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=3)
        return resp.text
    except Exception as e:
        return f"Failed to communicate with ESP32: {str(e)}"

@mcp.tool()
def get_device_status() -> str:
    """Retrieves uptime and health status from the ESP32."""
    url = f"http://{ESP32_IP}/status"
    try:
        resp = requests.get(url, timeout=2)
        return resp.text
    except Exception as e:
        return f"Device offline: {str(e)}"

if __name__ == "__main__":
    mcp.run()

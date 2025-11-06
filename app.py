from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
import os

DATA_HOST = os.getenv("DATA_HOST", "cmtx-api-data")
DATA_PORT = int(os.getenv("DATA_PORT", "8080"))

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello":
            try:
                with urlopen(f"http://{DATA_HOST}:{DATA_PORT}/data", timeout=5) as r:
                    payload = r.read()
                self.send_response(200); self.end_headers()
                self.wfile.write(b"API ▶ " + payload)
            except Exception as e:
                self.send_response(500); self.end_headers()
                self.wfile.write(f"api error: {e}".encode())
            return
        if self.path == "/health":
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok"); return
        self.send_response(404); self.end_headers()

if __name__ == "__main__":
    HTTPServer(("", 8080), H).serve_forever()
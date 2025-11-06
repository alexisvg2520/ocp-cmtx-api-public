from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import os

DATA_HOST = os.getenv("DATA_HOST", "cmtx-api-data")
DATA_PORT = int(os.getenv("DATA_PORT", "8080"))
DATA_URL  = f"http://{DATA_HOST}:{DATA_PORT}/data"

class Handler(BaseHTTPRequestHandler):
    def _write(self, status: int, text: str, content_type: str = "text/plain; charset=utf-8"):
        body = text.encode("utf-8", "replace")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._write(200, "ok")
            return

        if self.path == "/hello":
            try:
                req = Request(DATA_URL, headers={"User-Agent": "cmtx-api-public"})
                with urlopen(req, timeout=5) as resp:
                    payload_bytes = resp.read()           # bytes desde DATA
                payload_text = payload_bytes.decode("utf-8", "replace")
                self._write(200, f"API -> {payload_text}")
            except HTTPError as e:
                self._write(502, f"api error: upstream returned HTTP {e.code}")
            except URLError as e:
                self._write(502, f"api error: upstream unreachable ({e.reason})")
            except Exception as e:
                self._write(500, f"api error: {e}")
            return

        self._write(404, "not found")

if __name__ == "__main__":
    port = 8080
    print(f"cmtx-api-public listening on {port}, forwarding to {DATA_URL}")
    HTTPServer(("", port), Handler).serve_forever()
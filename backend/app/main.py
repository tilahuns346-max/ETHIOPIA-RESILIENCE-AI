import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from backend.app.router import Router

router = Router()

class ResilienceRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Idempotency-Key, X-Sync-Batch-ID")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def handle_request(self, method: str):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed_url.query).items()}
        
        handler, path_params = router.resolve(method, path)
        if not handler:
            self.send_response(404)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "message": f"Endpoint not found: {method} {path}"}).encode("utf-8"))
            return

        body = None
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(raw_body)
            except Exception:
                body = raw_body

        req = {
            "method": method,
            "path": path,
            "path_params": path_params,
            "query_params": query_params,
            "headers": dict(self.headers),
            "body": body
        }

        try:
            status_code, resp_body = handler(req)
            self.send_response(status_code)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp_body, default=str).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "INTERNAL_SERVER_ERROR", "error": str(e)}).encode("utf-8"))

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def do_DELETE(self):
        self.handle_request("DELETE")

def run_server(host="0.0.0.0", port=8000):
    server = HTTPServer((host, port), ResilienceRequestHandler)
    print(f"Ethiopia Resilience AI Backend running on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()

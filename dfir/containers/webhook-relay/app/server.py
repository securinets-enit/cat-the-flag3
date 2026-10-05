#!/usr/bin/env python3
"""
Webhook Relay — forward HTTP events between systems.
Author: 7ankalis — Securinets ENIT
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"webhook-relay 2.4.0\n")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"received": True, "bytes": len(body)}).encode())

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("[*] webhook-relay listening on :8080", flush=True)
    server.serve_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class ReviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)
        if request.path != "/review":
            self.send_error(404)
            return

        submitted_url = parse_qs(request.query).get("url", [""])[0]
        body = f"""<!doctype html>
<html><body><h1>Request received</h1>
<p>The backend review queue received:</p>
<code>{submitted_url}</code>
<p>An administrator will visit the submitted address during the next review window.</p>
<p>No server-side fetch was performed.</p>
<p><a href="/ssrf.html">Back to request form</a></p></body></html>"""
        encoded = body.encode()
        self.send_response(202)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format_string, *args):
        print(f"backend: {self.address_string()} - {format_string % args}", flush=True)

HTTPServer(("0.0.0.0", 8080), ReviewHandler).serve_forever()
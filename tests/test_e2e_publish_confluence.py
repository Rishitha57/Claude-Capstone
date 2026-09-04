import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class ConfluenceStubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = json.dumps({"results": []}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(content_length))
        assert body["type"] == "page"
        payload = json.dumps({"id": "e2e-page"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *_args):
        return


def test_publish_cli_creates_confluence_page_end_to_end(tmp_path):
    server = ThreadingHTTPServer(("127.0.0.1", 0), ConfluenceStubHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        html_path = tmp_path / "report.html"
        html_path.write_text("<h1>Workflow report</h1>", encoding="utf-8")
        project_root = Path(__file__).parents[1]
        environment = {
            **os.environ,
            "CONFLUENCE_BASE_URL": f"http://127.0.0.1:{server.server_port}",
            "CONFLUENCE_SPACE_KEY": "TEST",
            "CONFLUENCE_EMAIL": "test@example.com",
            "CONFLUENCE_API_TOKEN": "e2e-token",
        }

        result = subprocess.run(
            [
                sys.executable,
                "scripts/publish_confluence.py",
                str(html_path),
                "--title",
                "E2E Report",
            ],
            cwd=project_root,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert "e2e-page" in result.stdout
        assert "E2E Report" in result.stdout
    finally:
        server.shutdown()
        server.server_close()

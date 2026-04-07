import json
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from security_wrapper.audit import AuditLogger
from security_wrapper.siem import WebhookSiemForwarder


class _Collector:
    def __init__(self):
        self.payloads = []


class _Handler(BaseHTTPRequestHandler):
    collector = None

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        if _Handler.collector is not None:
            _Handler.collector.payloads.append(json.loads(body.decode("utf-8")))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return


class TestSiemForwarding(unittest.TestCase):
    def test_webhook_ingestion(self):
        collector = _Collector()
        _Handler.collector = collector
        server = HTTPServer(("127.0.0.1", 0), _Handler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        try:
            forwarder = WebhookSiemForwarder(
                endpoint=f"http://127.0.0.1:{port}/siem/events", timeout_seconds=2
            )
            logger = AuditLogger("/tmp/test_security_audit.jsonl", forwarder=forwarder)
            logger.log("siem_test", {"k": "v"})
            time.sleep(0.1)
            self.assertGreaterEqual(len(collector.payloads), 1)
            self.assertEqual(collector.payloads[0]["event_type"], "siem_test")
        finally:
            server.shutdown()
            thread.join(timeout=1)
            server.server_close()


if __name__ == "__main__":
    unittest.main()

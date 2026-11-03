"""Non-durable local project adapter mock. Not a Dynamics service."""

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAX_BODY_BYTES = 16384
FIELDS = {"externalMessageId", "eventType", "sourceApplication", "patientReference"}
PROJECTS = {"project-a", "project-b"}


class MockServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address):
        super().__init__(address, MockHandler)
        self.events = {project: [] for project in PROJECTS}
        self.event_lock = threading.Lock()


class MockHandler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, format, *args):
        pass

    def reply(self, status, body):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def project(self):
        parts = self.path.split("/")
        if len(parts) == 4 and parts[1] == "projects" and parts[3] == "events":
            return parts[2]
        return None

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, {"ready": True, "service": "non-durable-local-mock"})
            return
        project = self.project()
        if project not in PROJECTS:
            self.reply(404, {"error": "Unknown route"})
            return
        with self.server.event_lock:
            events = list(self.server.events[project])
        self.reply(200, events)

    def do_POST(self):
        project = self.project()
        if project == "failing":
            self.reply(503, {"error": "Deliberate adapter failure"})
            return
        if project not in PROJECTS:
            self.reply(404, {"error": "Unknown route"})
            return
        if self.headers.get("Transfer-Encoding"):
            self.reply(400, {"error": "Use bounded Content-Length, not transfer encoding"})
            return
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self.reply(411, {"error": "Valid Content-Length required"})
            return
        if not 0 < length <= MAX_BODY_BYTES:
            self.reply(413, {"error": "Request body outside permitted size"})
            return
        if self.headers.get_content_type() != "application/json":
            self.reply(415, {"error": "Content-Type must be application/json"})
            return
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError("Incomplete body")
            event = json.loads(raw)
        except (ValueError, UnicodeError):
            self.reply(400, {"error": "Invalid JSON"})
            return
        except OSError:
            self.reply(408, {"error": "Request body deadline exceeded"})
            return
        if (
            not isinstance(event, dict)
            or set(event) != FIELDS
            or any(not isinstance(value, str) or not value.strip() for value in event.values())
            or event["eventType"] != "ADT^A01"
        ):
            self.reply(422, {"error": "Expected four nonempty demo fields and eventType ADT^A01"})
            return
        with self.server.event_lock:
            self.server.events[project].append(event)
        self.reply(201, {"recorded": True})


def main():
    try:
        with MockServer(("127.0.0.1", 8081)) as server:
            print("NON-DURABLE LOCAL MOCK (not Dynamics) http://127.0.0.1:8081", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except OSError as error:
        print(f"MOCK_FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

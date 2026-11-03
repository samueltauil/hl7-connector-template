import concurrent.futures
import http.client
import json
import sys
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from mock_destination import MockServer, MAX_BODY_BYTES

EVENT = {
    "externalMessageId": "DEMO-A-001",
    "eventType": "ADT^A01",
    "sourceApplication": "LAB-A",
    "patientReference": "SYNTH-A-100",
}


class MockTest(unittest.TestCase):
    def setUp(self):
        self.server = MockServer(("127.0.0.1", 0))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.close)

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.assertFalse(self.thread.is_alive())

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def post(self, project, event=EVENT):
        return self.request(
            "POST", f"/projects/{project}/events", json.dumps(event), {"Content-Type": "application/json"}
        )

    def test_readiness_and_separate_collections(self):
        self.assertEqual((200, {"ready": True, "service": "non-durable-local-mock"}), self.request("GET", "/health"))
        self.assertEqual(201, self.post("project-a")[0])
        self.assertEqual((200, [EVENT]), self.request("GET", "/projects/project-a/events"))
        self.assertEqual((200, []), self.request("GET", "/projects/project-b/events"))
        self.assertEqual(201, self.post("project-b", {**EVENT, "externalMessageId": "DEMO-B-001"})[0])
        self.assertEqual(1, len(self.request("GET", "/projects/project-a/events")[1]))

    def test_repeated_and_concurrent_events_are_not_deduplicated(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            outcomes = list(executor.map(lambda _: self.post("project-a")[0], range(8)))
        self.assertEqual([201] * 8, outcomes)
        self.assertEqual(8, len(self.request("GET", "/projects/project-a/events")[1]))

    def test_failure_route_records_nothing(self):
        self.assertEqual(503, self.post("failing")[0])
        self.assertEqual((200, []), self.request("GET", "/projects/project-a/events"))
        self.assertEqual((200, []), self.request("GET", "/projects/project-b/events"))

    def test_unknown_routes_are_explicit(self):
        self.assertEqual(404, self.request("GET", "/unknown")[0])
        self.assertEqual(404, self.post("unknown")[0])

    def test_invalid_json_media_type_and_size(self):
        self.assertEqual(400, self.request("POST", "/projects/project-a/events", "{", {"Content-Type": "application/json"})[0])
        self.assertEqual(415, self.request("POST", "/projects/project-a/events", "{}")[0])
        self.assertEqual(413, self.request("POST", "/projects/project-a/events", "x" * (MAX_BODY_BYTES + 1), {"Content-Type": "application/json"})[0])
        self.assertEqual((200, []), self.request("GET", "/projects/project-a/events"))

    def test_invalid_contract_is_not_recorded(self):
        for event in ({}, [], {**EVENT, "patientReference": ""}, {**EVENT, "eventType": "ADT^A08"},
                      {**EVENT, "rawMessage": "not allowed"}, {**EVENT, "sourceApplication": 10}):
            with self.subTest(event=event):
                self.assertEqual(422, self.post("project-a", event)[0])
        self.assertEqual((200, []), self.request("GET", "/projects/project-a/events"))


if __name__ == "__main__":
    unittest.main()

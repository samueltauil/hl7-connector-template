import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import send_hl7

MESSAGE = "MSH|^~\\&|LAB-A|LOCAL|APP|LOCAL|20261103090000||ADT^A01|DEMO-A-001|P|2.5\nPID|1||SYNTH-A-100\n"
ACK = b"\x0bMSH|^~\\&|APP|LOCAL|LAB-A|LOCAL|20261103090000||ACK|ACK-1|P|2.5\rMSA|AA|DEMO-A-001\r\x1c\x0d"


class SenderTest(unittest.TestCase):
    def connection(self, chunks):
        connection = MagicMock()
        connection.__enter__.return_value = connection
        connection.recv.side_effect = chunks
        return connection

    def test_normalizes_all_fixture_line_endings(self):
        for ending in ("\n", "\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                result = send_hl7.normalize(MESSAGE.replace("\n", ending))
                self.assertNotIn("\n", result)
                self.assertTrue(result.endswith("\r"))
                self.assertNotIn("\r\r", result)
                self.assertEqual("DEMO-A-001", send_hl7.control_id(result))

    def test_sendall_and_partial_ack_reads(self):
        connection = self.connection([ACK[:3], ACK[3:-1], ACK[-1:]])
        with patch("send_hl7.socket.create_connection", return_value=connection):
            self.assertEqual(("AA", "DEMO-A-001"), send_hl7.send_message("127.0.0.1", 2575, MESSAGE, "AA", 5))
        connection.sendall.assert_called_once_with(
            b"\x0b" + send_hl7.normalize(MESSAGE).encode() + b"\x1c\x0d"
        )
        connection.__exit__.assert_called_once()

    def test_wrong_type_and_correlation_fail(self):
        for ack in (ACK.replace(b"MSA|AA", b"MSA|AR"), ACK.replace(b"MSA|AA|DEMO-A-001", b"MSA|AA|OTHER")):
            with self.subTest(ack=ack):
                with self.assertRaises(ValueError):
                    send_hl7.parse_ack(ack, "DEMO-A-001", "AA")

    def test_malformed_ack_and_closed_connection_fail(self):
        for chunks in ([b"bad"], [ACK[:-2], b""], [b"\x0bMSH|x\r\x1c\x0d"]):
            with self.subTest(chunks=chunks):
                with patch("send_hl7.socket.create_connection", return_value=self.connection(chunks)):
                    with self.assertRaises(ValueError):
                        send_hl7.send_message("127.0.0.1", 2575, MESSAGE, "AA", 1)

    def test_socket_timeout_is_not_success(self):
        with patch("send_hl7.socket.create_connection", return_value=self.connection([socket.timeout("deadline")])):
            with self.assertRaises(TimeoutError):
                send_hl7.send_message("127.0.0.1", 2575, MESSAGE, "AA", 0.1)

    def test_oversized_ack_fails(self):
        chunks = [b"\x0b" + b"x" * send_hl7.MAX_ACK_BYTES]
        with patch("send_hl7.socket.create_connection", return_value=self.connection(chunks)):
            with self.assertRaisesRegex(ValueError, "limit"):
                send_hl7.send_message("127.0.0.1", 2575, MESSAGE, "AA", 1)

    def test_duplicate_msa_and_trailing_data_fail(self):
        for ack in (ACK.replace(b"\x1c\x0d", b"MSA|AA|DEMO-A-001\r\x1c\x0d"), ACK + b"extra"):
            with self.subTest(ack=ack):
                with self.assertRaises(ValueError):
                    send_hl7.parse_ack(ack, "DEMO-A-001", "AA")

    def test_invalid_fixture_is_rejected(self):
        for fixture in ("\ufeff" + MESSAGE, MESSAGE + "\x0b", MESSAGE.replace("\nPID", "\n\nPID")):
            with self.subTest(fixture=fixture):
                with self.assertRaises(ValueError):
                    send_hl7.normalize(fixture)
        with self.assertRaises(ValueError):
            send_hl7.control_id("PID|1\r")


if __name__ == "__main__":
    unittest.main()

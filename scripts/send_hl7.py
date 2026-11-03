"""Synthetic MLLP client. A wire ACK is successful only with matching MSA-2."""

import argparse
import socket
import sys
import time
from pathlib import Path

START = b"\x0b"
END = b"\x1c\x0d"
MAX_ACK_BYTES = 65536


def normalize(text):
    if text.startswith("\ufeff"):
        raise ValueError("Fixture must not contain a UTF-8 BOM")
    if any(char in text for char in ("\x0b", "\x1c", "\x00")):
        raise ValueError("Fixture must contain unframed HL7 text")
    segments = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n").split("\n")
    if not segments or any(not segment for segment in segments):
        raise ValueError("Fixture contains an empty segment")
    return "\r".join(segments) + "\r"


def control_id(payload):
    first = payload.split("\r", 1)[0]
    if not first.startswith("MSH|"):
        raise ValueError("Fixture must start with an MSH using the lab's | separator")
    fields = first.split("|")
    if len(fields) <= 9 or not fields[9]:
        raise ValueError("Fixture is missing MSH-10")
    return fields[9]


def parse_ack(frame, expected_id, expected_type):
    if not frame.startswith(START) or not frame.endswith(END):
        raise ValueError("Malformed MLLP ACK framing")
    payload = frame[1:-2].decode("utf-8")
    if "\x0b" in payload or "\x1c" in payload or not payload.startswith("MSH|"):
        raise ValueError("Malformed ACK payload")
    msa = [segment.split("|") for segment in payload.split("\r") if segment.startswith("MSA|")]
    if len(msa) != 1 or len(msa[0]) < 3:
        raise ValueError("ACK must contain exactly one MSA with MSA-1 and MSA-2")
    ack_type, ack_id = msa[0][1:3]
    if ack_id != expected_id:
        raise ValueError(f"ACK correlation mismatch: expected {expected_id}, received {ack_id}")
    if ack_type != expected_type:
        raise ValueError(f"ACK type mismatch: expected {expected_type}, received {ack_type}")
    return ack_type, ack_id


def send_message(host, port, text, expect, timeout):
    if timeout <= 0:
        raise ValueError("Timeout must be positive")
    payload = normalize(text)
    message_id = control_id(payload)
    deadline = time.monotonic() + timeout
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(max(0.001, deadline - time.monotonic()))
        connection.sendall(START + payload.encode("utf-8") + END)
        response = bytearray()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Deadline reached before complete ACK")
            connection.settimeout(remaining)
            chunk = connection.recv(min(4096, MAX_ACK_BYTES + 1 - len(response)))
            if not chunk:
                raise ValueError("Connection closed before complete ACK")
            response.extend(chunk)
            if len(response) > MAX_ACK_BYTES:
                raise ValueError("ACK exceeds response limit")
            if response[0:1] != START:
                raise ValueError("ACK does not start with MLLP start byte")
            if END in response:
                if not response.endswith(END) or response.count(END) != 1:
                    raise ValueError("Unexpected trailing data in ACK")
                return parse_ack(bytes(response), message_id, expect)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--expect", choices=("AA", "AE", "AR"), required=True)
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()
    try:
        ack, message_id = send_message(
            args.host, args.port, args.file.read_text(encoding="utf-8"), args.expect, args.timeout
        )
    except (OSError, ValueError, UnicodeError) as error:
        print(f"SEND_FAILED: {error}", file=sys.stderr)
        return 1
    print(f"ACK={ack} MESSAGE_ID={message_id} CORRELATION=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

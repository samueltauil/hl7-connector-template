# Protocol notes

The fixtures are synthetic HL7 v2.5 ER7 text. The sender normalizes LF/CRLF into
CR segment delimiters and adds exactly `0x0B + message + 0x1C + 0x0D`.
Do not store MLLP framing or a UTF-8 BOM in fixtures.

ACK MSA-1 carries AA/AE/AR; MSA-2 must match the original MSH-10. Checking an
exchange property is insufficient: `send_hl7.py` inspects a complete ACK
frame received through a socket. The sender has one overall deadline and a
64 KiB response limit, and fails on incomplete or uncorrelated ACKs.

Camel's MLLP consumer generates the acknowledgment from the original message.
Control its outcome with the exchange **property**
`CamelMllpAcknowledgementType`, using `MllpConstants.MLLP_ACKNOWLEDGEMENT_TYPE`
where available. Do not use a similarly named message header or assume changing
the message body controls the wire ACK. Keep ACK-related exchange properties
when replacing outbound HTTP headers.

Use original-mode application acknowledgments:
AA after synchronous adapter HTTP 2xx; AR for parseable policy/required-field
rejection; AE for HTTP failure, timeout, or internal processing failure.
Handled exceptions must explicitly retain the negative outcome. Disable route
redelivery, bound HTTP connect/response timeouts, and log safe metadata only.

HAPI `hapi-structures-v25` must match Camel's `hapi-base` dependency: both are
2.6.0 here. Parse using HAPI; retain the parsed Message internally. Never serialize
it as downstream JSON. A08 deliberately uses the valid `ADT_A01` structure for
HL7 2.5: rejection must come from the configured A01-only policy.

Malformed frames can lack an ID or valid MSH. Do not promise a correlated AR for
arbitrary bytes. Use the parseable unsupported fixture for the live rejection.

Refer to the MLLP, HL7, Camel Main, and Route Template sources in
[Official sources](official-sources.md). This is a prototype contract, not a
general HL7 conformance profile.

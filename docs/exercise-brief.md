# Exercise brief

Build one reusable HL7 v2.5 MLLP listener component. Keep project mappings in a
separate adapter. Demonstrate reuse by adding Project B through configuration,
without changing Java. Use synthetic data and a local HTTP mock only.

Keep the workshop small: generate the running app, not a JUnit suite. Use the
existing three verification stages to prove real delivery, reuse, and rejection.

### Stack

| Piece | Implementation | Reason |
| --- | --- | --- |
| Runtime | Java 21 and Camel Main | Small standalone Java project |
| Camel release | Pin 4.22.2 LTS for the initial rehearsal | Supported LTS listed on the official download page on November 3, 2026 [S1] |
| MLLP transport | `camel-mllp` | Use its consumer and ACK support [S2] |
| HL7 parsing | `camel-hl7` and matching `hapi-structures-v25` | HAPI parsing and the model library for the fixture version [S3] |
| Reuse mechanism | Camel route templates | Instantiate routes from parameters [S4] |
| Configuration | Camel Main `application.properties` | Native configuration, including route-template instances [S4, S5] |
| Downstream adapter | `camel-http`, `camel-jackson`, and `camel-direct` | Synchronous local HTTP delivery, outside the listener |
| Logging | One SLF4J implementation | Metadata-only diagnostics |
| Demo proof | Existing `verify-demo.ps1` stages | Real ACK, JSON, isolation, and rejection checks |
| Supporting tools | Python 3 standard library | No additional Python package installation |
| Build | Maven Wrapper, pinned Maven and plugin versions | Repeatable Windows commands |

### Visual Studio workflow for this Java project

Keep Camel rather than silently converting the exercise to .NET. Open the
repository using **File > Open > Folder** in Visual Studio [S11]. Use Copilot
for reading and editing files, and Maven commands for compiling, testing, and
running the application.

This is a folder-based Java/Maven lab, not a Visual Studio .NET solution.
Do not instruct participants to create a `.sln`, press F5, build through
**Build Solution**, or run JUnit through Visual Studio Test Explorer.
Do not require Java symbol tools or an additional Java IDE extension.

Before distributing the template, rehearse Copilot file discovery, Java-file
editing, and Maven terminal execution in this exact Visual Studio folder
workflow. Open Folder support alone does not prove every Copilot action works
for this scaffold. If a required action fails, fix and re-rehearse the lab before
inviting participants; do not switch them to another IDE during the session.

Dependency/plugin versions are already pinned in the POM and
`docs\environment.md`. Use them unchanged. HAPI base and v2.5 structures are
aligned at 2.6.0.

### Architecture

```text
                     REUSABLE LISTENER TEMPLATE
Synthetic sender --> MLLP --> HAPI parsing --> acceptance rules --> internal envelope
                        ^                                             |
                        |                                             v
                 correlated HL7 ACK                         configurable adapter URI
                                                                      |
                                                       PROJECT ADAPTER TEMPLATE
                                                                      |
                                                         mapping --> JSON --> HTTP
                                                                      |
                                                            local project mock
```

Use two route templates:

| Template | Parameters | Responsibility |
| --- | --- | --- |
| `hl7-listener` | `listenerId`, `host`, `port`, `acceptedMessageType`, `adapterUri` | Receive, parse, apply acceptance policy, build envelope, invoke adapter, control ACK outcome |
| `demo-http-adapter` | `adapterId`, `destinationUrl` | Consume a `direct:` endpoint, map the envelope, deliver JSON |

The listener does not know a Dynamics entity name, an HTTP destination, or
project-specific mapping rules. Its boundary is the configurable adapter URI.
The two projects may reuse the same demo adapter template with different
destinations. A future real Dynamics adapter can replace that template without
changing the listener.

Do not introduce a custom list-binding configuration framework or manually
instantiate a hardcoded pair of projects in Java. Camel supports route-template
instances in `application.properties` [S4].

### Internal envelope and external payload

Propose an internal Java envelope with:

| Field | Source |
| --- | --- |
| `messageId` | MSH-10 |
| `messageType` | MSH-9.1 plus MSH-9.2, for example `ADT^A01` |
| `sendingApplication` | MSH-3 |
| `sendingFacility` | MSH-4 |
| `receivedAt` | UTC instant captured at receipt |
| `message` | Parsed HAPI `Message`, retained internally for the adapter |

Do not serialize the entire HAPI object to JSON. The adapter creates a separate
DTO containing `externalMessageId`, `eventType`, `sourceApplication`, and a
synthetic `patientReference` extracted from PID-3.1. This is an illustrative
mapping, not a real Dynamics API contract.

For this demo, require messageId, messageType, sendingApplication,
sendingFacility, and PID-3.1 to be nonempty. Reject a parseable missing-field
message with AR before invoking the adapter.

Build an explicit outbound HTTP header allowlist, rather than forwarding all
HL7/Camel headers. Preserve the exchange properties needed for acknowledgment
generation when cleaning message headers.

The supplied mock accepts a JSON body of at most 16 KiB with `Content-Length`;
it rejects chunked transfer encoding. Send a fixed-length JSON body from the
adapter, not an unknown-length stream.

Keep patient fields out of listener logs and error messages. Synthetic values
can appear in the deliberately local mock's inspection response.

### Acknowledgment contract

Use original-mode application acknowledgments for this prototype:

| Situation | Result | Destination effect |
| --- | --- | --- |
| Supported, valid message and adapter HTTP 2xx | `AA` | One event recorded |
| Parseable but unsupported message type | `AR` | No event |
| Parseable message missing a required demo field | `AR` | No event |
| Adapter HTTP error or timeout | `AE` | No success claim |

`AA` means synchronous validation and successful response from the configured
demo adapter. It does not mean durable storage or actual Dynamics processing.

Set the documented `CamelMllpAcknowledgementType` exchange property, preferably
through Camel's constant, when controlling Camel's generated ACK [S2].
Do not assume that replacing the message body or setting a similarly named
header controls the wire ACK.

A handled exception must still result in the correct negative acknowledgment.
No broad catch that turns failures into `AA`. Use bounded HTTP timeouts and
disable route redelivery for the demonstration to keep failures predictable.

Make MSA-2 correlation to the original MSH-10 an acceptance criterion. Check
the actual ACK sent over a socket, not only an exchange property.

Malformed or incomplete frames may not contain enough information to generate
a correlated ACK. Do not promise an
`AR` for every arbitrary byte sequence. Use a valid, unsupported fixture for the
live negative example.

### Configuration examples

Project A only, created during application implementation:

```properties
camel.main.name=hl7-integration-lab
camel.main.base-package-scan=lab.hl7

camel.route-template[0].template-id=hl7-listener
camel.route-template[0].listenerId=project-a
camel.route-template[0].host=127.0.0.1
camel.route-template[0].port=2575
camel.route-template[0].acceptedMessageType=ADT^A01
camel.route-template[0].adapterUri=direct:project-a

camel.route-template[1].template-id=demo-http-adapter
camel.route-template[1].adapterId=project-a
camel.route-template[1].destinationUrl=http://127.0.0.1:8081/projects/project-a/events
```

Project B is later added by appending:

```properties
camel.route-template[2].template-id=hl7-listener
camel.route-template[2].listenerId=project-b
camel.route-template[2].host=127.0.0.1
camel.route-template[2].port=2576
camel.route-template[2].acceptedMessageType=ADT^A01
camel.route-template[2].adapterUri=direct:project-b

camel.route-template[3].template-id=demo-http-adapter
camel.route-template[3].adapterId=project-b
camel.route-template[3].destinationUrl=http://127.0.0.1:8081/projects/project-b/events
```

Verify this exact spelling and startup discovery with the pinned Camel release
during rehearsal. Let Camel assign unique internal node IDs, or verify a
template-safe naming strategy; repeated fixed node IDs can break reuse.

This exercise demonstrates configuration-based reuse at startup. Stop and
restart the application after adding Project B. Do not claim hot reload.

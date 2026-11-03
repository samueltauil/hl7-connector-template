# Acceptance criteria

The complete application must satisfy all of these, not merely open a TCP port.

| Outcome | Proof |
| --- | --- |
| Project A accepts valid ADT^A01 | Real MLLP ACK has MSA-1 `AA` and MSA-2 equal to MSH-10 |
| Correct adapter boundary | Four-field JSON reaches only Project A's HTTP destination |
| Project B is configuration-only | Append native listener/adapter instances, restart, no Java changes |
| Both instances isolated | Real sockets on separate loopback ports, separate destination arrays |
| Unsupported message rejected | Valid ADT^A08 gives correlated `AR`, no downstream event |

Keep the generated app small. Do not create automated test classes or add test
dependencies. Compile with `.\mvnw.cmd -q compile`, then demonstrate the real
running solution with all three existing stages in order:

```powershell
.\scripts\verify-demo.ps1 -Stage A
# Add B through configuration and restart App, leaving Mock running.
.\scripts\verify-demo.ps1 -Stage Both
.\scripts\verify-demo.ps1 -Stage Reject
```

Stage A persists all Java paths/hashes in ignored `.lab-runtime\java-baseline.json`.
Stage Both fails if any Java file is added, removed, or changed.
Every delivery check uses before/after counts, so repeated sends are not mistaken
for deduplication. `AA` means synchronous demo HTTP success, not durable storage.

The implementation must still follow the brief's AA/AE/AR contract, bound HTTP
timeouts, keep mapping outside the listener, and avoid raw-message logging.
Do not edit scripts or fixtures just to make the output green.
The three stages prove the workshop scenario, not every production failure mode.

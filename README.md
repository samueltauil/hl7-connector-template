# HL7 Integration Lab

Build a reusable HL7 v2 MLLP listener with GitHub Copilot in Visual Studio.
Prove reuse by adding a second project through configuration, without changing
Java. Each developer works in their own repository and runs their own local mock.

**This is the starting template, not the application.** There is no `src` code
and no active Copilot customization. Copilot creates both during the lab.
The mock is synthetic, local, in-memory, and **not a Dynamics service**.

## Start here

1. Create your own repository from this template, then clone it.
2. Open the repository root using **File > Open > Folder** in Visual Studio.
3. Follow [Environment setup](docs/environment.md), then run in PowerShell:

   ```powershell
   .\scripts\warmup.ps1
   .\scripts\preflight.ps1
   ```

4. Follow the [Participant guide](docs/participant-guide.md). It contains the
   exact Copilot prompts, terminal commands, checkpoints, and troubleshooting.

Use Visual Studio 2026 **18.5 or later**, a Java **21 JDK**, Git, Python **3.10+**,
and your own Copilot access. See the environment document for the actual rehearsal
build and any differences. Maven is provided through the pinned wrapper.
Ports **2575, 2576, 8081** must be free.

## What proves the result

| Check | Evidence |
| --- | --- |
| Project A | Correlated wire `AA` and correct downstream JSON |
| Project B | Both listeners route only to their own destinations |
| Reuse | All application/test Java paths and SHA-256 hashes unchanged |
| Rejection | Correlated `AR` for a valid unsupported message; no new events |

`AA` means synchronous demo-adapter success, not durable intake or production
interoperability. No real data, tenant, cloud service, persistence, or runtime LLM
is involved.

## Repository map

| Resource | Purpose |
| --- | --- |
| [Exercise brief](docs/exercise-brief.md) | Listener/adapter boundary and exact contract |
| [Acceptance criteria](docs/acceptance-criteria.md) | Required application behavior and tests |
| [Copilot customization notes](docs/copilot-customizations.md) | Roles and review checks, not prewritten files |
| `fixtures` | Four synthetic HL7 v2.5 messages |
| `scripts` | Mock, MLLP sender, readiness and end-to-end verification |
| `support-tests` | Tests for the supplied support tools |
| [Facilitator guide](docs/facilitator-guide.md) | Pacing, recovery, and readiness limitations |
| [Official sources](docs/official-sources.md) | Primary documentation inventory |
| [Rehearsal evidence](docs/rehearsal.md) | Observed results, screenshots, and remaining gates |

Scaffold checks:

```powershell
.\mvnw.cmd -q validate
python -m unittest discover -s .\support-tests -p "test_*.py"
```

After Copilot creates the small application, use `.\mvnw.cmd -q compile`, then
run the three demo-verification stages from the guide. No generated JUnit suite
is required. Compilation is not runtime proof; the existing scripts check real
ACKs and delivered JSON. CI checks only scaffold integrity and support tools.

Local creation does not publish anything to GitHub. When the organizer chooses
to publish, enable **Settings > General > Template repository**. Share the actual
template URL; never have participants start from a reference solution.

# Rehearsal evidence

Completed the core runtime rehearsal on November 3, 2026, in a separate local
copy. Visual Studio Copilot generated the application and its repair. All three
demo checks passed in Visual Studio's terminal. The automation limitations below
matter: this was not a timed participant pilot or a flawless UI-only run.

## Environment observed

Windows 11; Visual Studio Enterprise 2026 installation version
18.11.12328.437 (terminal banner: v18.11.3); Temurin JDK 25.0.5;
Python 3.14.10; Maven Wrapper 3.9.11.
The Java compilation target remains release 21. Java 21 runtime rehearsal is
a separate organizer gate.

## Starting scaffold

Maven validate, dependency warmup, preflight, and 14 Python support tests passed.
The template intentionally has no application source or active Copilot files.
After the requested workshop simplification, participants generate no JUnit suite.
The separate copy contains the generated customizations and application. The
starting template still contains neither. No application test suite or new
dependency was needed.

## Results

| Step | Observed result |
| --- | --- |
| Create customizations | Five requested files generated, kept, saved, and present on disk |
| Ask Integration Architect | Agent selectable; design separates listener and adapter, explains ACKs and configuration-only reuse |
| Implement Project A | Four Java files and properties generated; Maven compilation passed |
| Verify Project A | First run exposed an HTTP framing bug; passed after Copilot's repair and restart |
| Add Project B | Attached the saved prompt through **+ Add reference**; only `application.properties` changed |
| Verify both projects | Both returned correlated AA ACKs, delivered to separate destinations, and retained the Stage A Java hashes |
| Verify rejection | Unsupported message returned correlated AR; event counts did not increase |

The final terminal output was:

```text
STAGE_A=PASS ACK=AA CORRELATION=OK DELIVERY=OK
STAGE_BOTH=PASS ACK_A=AA ACK_B=AA ISOLATION=OK JAVA_CHANGES=0
STAGE_REJECT=PASS ACK=AR CORRELATION=OK NEW_EVENTS=0
```

These are real wire checks against the supplied local mock. They do not prove
durability, production readiness, every malformed-message case, or timeout
behavior. Explicit skill use was requested; this record does not claim that a
separate skill-activation indicator was verified.

## Visual Studio computer-use observations

Computer use observed the running instance and its Agent chat panel. It exposed
only a sparse accessibility tree (no menu, chat input, or terminal input nodes).
Indexed and screenshot-coordinate clicks reported completion but produced no
visible UI change. Keyboard and text insertion attempts returned
`no_viable_candidate`; the system-menu action was also rejected.

On retry, after the user opened the rehearsal folder, the full accessibility
tree became available. Folder View showed the expected scaffold, and selecting
Chat and inserting the exact Step 2 customization prompt succeeded. The prompt
was left unsent during that attempt. Selecting the Developer PowerShell tab worked, but its terminal
input again returned `no_viable_candidate`. Its current directory was still
`source\repos`, confirming why the guide requires setting each terminal's path.

No Copilot request was submitted during those early attempts.

At the user's request, the guide was subsequently changed to short,
natural-language prompts. The prewritten customization recipes were removed,
and the rehearsal clone was updated. Another computer-use retry exposed only
the sparse tree again; the system-menu action failed with
`UIA ExpandCollapse.Expand failed: 0x80131509`.

After Visual Studio restarted, computer use regained access to the chat controls.
The updated natural-language Step 2 prompt was submitted successfully. Copilot
reported GPT-6 Luna for that response and created all five customization files.
The edits were kept and **Save All** was used. A subsequent filesystem check
confirmed the five files persisted and `src` was still absent. Copilot also
updated `docs\copilot-customizations.md` in the rehearsal copy.

The generated architect declares `tools: [code_search, readfile]`. It appeared
in the agent picker and was selected in a new chat. It answered the Step 3 design
prompt without creating Java. Implementation then used the general Agent.

Copilot attempted **Build Solution** during customization setup. That operation
was denied because this is an Open Folder Java/Maven workshop. Maven compilation
later passed. Participants should use the Maven command in Step 4.

A real Visual Studio window screenshot was captured through computer use with
Alt+Print Screen, pasted into Paint, and saved as PNG. Crops of the generated
agent header and agent picker are embedded in Step 2 of the participant guide.
The crops omit the account avatar and unrelated window chrome. They document
customization creation and discovery only, not a running integration.

Developer PowerShell later crashed in PSReadLine during automated input.
Developer Command Prompt worked with `pwsh -NoProfile -File` for the supplied
scripts. Mock startup, app startup, and all three passing checks ran through
Visual Studio terminals. The guide now includes this terminal fallback.

Automated Ctrl+C failed. The rehearsal stopped only the identified lab Java
process by PID before restarting; the manual Ctrl+C step was not validated by
automation. A later Return delivery delay caused a readiness failure before the
app started. A guarded shell fallback refused to start a duplicate once the
Visual Studio launch had succeeded. Rerunning Both and Reject then passed.

## Repairs and prompt adjustments

Project A initially compiled but returned AE instead of AA. The app logged
`HttpOperationFailedException`. Copilot found that marshalled JSON was an
unknown-length stream, while the mock rejects chunked transfer encoding.
It converted the body to `byte[]` and enforced the existing 16 KiB limit.
Compilation and Stage A then passed. The mock and verifier were not weakened.
The exercise brief now states the fixed-length HTTP body requirement explicitly.

The first short Project B request received an unexplained refusal. A follow-up
clarified that the exercise uses synthetic fixtures and a loopback mock, and
repeated the configuration-only scope. Copilot then added the two Project B
instances without changing Java, dependencies, fixtures, or scripts.
Customization generation reported GPT-6 Luna; implementation and repair used
GPT-6.1 Sol.

## Separate local copy

The starting template is the local Git repository in `hl7-connector-template`.
The fresh local rehearsal clone is `hl7-integration-lab-rehearsal-20261103-01`,
beside it, outside the template workspace. It started without application code or
active Copilot files and now contains the generated solution. Local Git tags
`rehearsal-project-a` and `rehearsal-project-b` preserve the passing checkpoints
in that separate repository. Nothing has
been published to GitHub; creating a repository
through GitHub's **Use this template** remains an organizer publication step.

## Publication gates

Do not advertise guaranteed AI output or a pilot-validated 35-minute exercise.
Before distributing the lab, finish two fresh Visual Studio generations and a
pilot with at least two developers who did not author it. Record elapsed times,
the selected model, file discovery, tool approvals, and repair time.

Never substitute an application implemented by a different Copilot client and
describe it as a Visual Studio rehearsal. Keep reference checkpoints outside
the starting template and disclose their use.

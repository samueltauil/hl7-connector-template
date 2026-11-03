# Rehearsal evidence

Prepared November 3, 2026. This record separates observed checks from untested
milestones. A scaffold pass is not an application pass.

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
The following stages still require the separate Visual Studio-generated copy:
customization creation, architect selection, skill activation, app compilation,
Stage A, configuration-only Project B, Stage Both, and Stage Reject.

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

No Copilot request was submitted, no application was generated, and no runtime
stage was passed through this instance. This must not be presented as a completed
step-by-step Visual Studio rehearsal. Resolve chat and terminal input access
before continuing; do not bypass computer use
with shell/UI automation or silently substitute another Copilot client.

At the user's request, the guide was subsequently changed to short,
natural-language prompts. The prewritten customization recipes were removed,
and the rehearsal clone was updated. Another computer-use retry exposed only
the sparse tree again; the system-menu action failed with
`UIA ExpandCollapse.Expand failed: 0x80131509`. The old recipe-based chat draft
has not been replaced or sent. Use the updated Step 2 prompt, not that stale draft,
when input is available.

Computer-use screenshots were captured in the session, but there are no verified
participant-step screenshots embedded in this template yet. Add those only after
the corresponding steps work; an empty Agent panel is not evidence of success.

## Separate local copy

The starting template is the local Git repository in `hl7-connector-template`.
The fresh local rehearsal clone is `hl7-integration-lab-rehearsal-20261103-01`,
beside it, outside the template workspace. It starts without application code or
active Copilot files. Nothing has been published to GitHub; creating a repository
through GitHub's **Use this template** remains an organizer publication step.

## Publication gates

Do not advertise guaranteed AI output or a pilot-validated 35-minute exercise.
Before distributing the lab, finish two fresh Visual Studio generations and a
pilot with at least two developers who did not author it. Record elapsed times,
the selected model, file discovery, tool approvals, and repair time.

Never substitute an application implemented by a different Copilot client and
describe it as a Visual Studio rehearsal. Keep reference checkpoints outside
the starting template and disclose their use.

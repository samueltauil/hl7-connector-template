# Participant guide: build your own solution in Visual Studio

Use Copilot to build an HL7 listener, send a sample message through it, and add
a second integration through configuration. You will work in your own repository
and use the supplied sample messages and local HTTP destination.

The listener receives HL7 messages over MLLP, a TCP-based transport, and returns
an acknowledgement (ACK). A project adapter maps each accepted message to JSON
and sends it to the local destination. The supplied checks let you confirm
delivery, reuse, and rejection without writing a test suite.

### Set up your repository and terminals

Follow [Environment setup](environment.md) to install the prerequisites and
sign in to Copilot, then create your working copy:

1. Open the `samueltauil/hl7-connector-template` repository on GitHub.
2. Select **Use this template > Create a new repository**.
3. Choose your own account and name the repository `hl7-integration-lab`.
   Choose your preferred visibility and leave **Include all branches** unchecked.
4. Create the repository and copy its clone URL from **Code > HTTPS**.
5. In Visual Studio, choose **Git > Clone Repository**, paste your repository
   URL, choose a local directory, and select **Clone** [S13].
6. Choose **File > Open > Folder** and open the cloned repository root [S11].
   You should see `pom.xml`, `docs`, `fixtures`, and `scripts` in Solution Explorer.
7. Select the **GitHub Copilot** badge at the top right and choose **Open Chat**.
   Check that you are signed in with Copilot access.
8. Open **Tools > Options > All Settings > GitHub > Copilot > Copilot Chat**.
   Enable **Enable custom instructions to be loaded from
   .github/copilot-instructions.md files and added to requests** [S6].
9. Open **View > Terminal** and select a PowerShell profile [S12].
   Run `Get-Location` to check the directory. If needed, run
   `Set-Location 'C:\path\to\hl7-integration-lab'`, replacing the example path
   with your clone's location. Use the repository root, not `src` or `scripts`.
10. Run these commands **one at a time**, including the
    `powershell.exe -NoProfile -File` prefix. Wait for warmup to finish before
    running preflight:

```powershell
powershell.exe -NoProfile -File .\scripts\warmup.ps1
powershell.exe -NoProfile -File .\scripts\preflight.ps1
```

Use this full command form for every `.ps1` script in the guide, whether your
Visual Studio terminal uses PowerShell or Developer Command Prompt.

Look for `WARMUP=PASS APPLICATION_FILES_CREATED=0`, then
`PREFLIGHT=PASS PORTS=FREE`. Warmup may take a few minutes while Maven downloads
dependencies. If the terminal reports that script execution is disabled, follow
the execution-policy guidance in [Environment setup](environment.md).

Both commands must succeed before you continue. If either fails, resolve the
reported problem using [Environment setup](environment.md), then run it again.

Use the terminal profile dropdown to open two more PowerShell terminals. Keep
three terminals available for these roles:

| Terminal | Purpose |
| --- | --- |
| Mock | Runs the local HTTP destination |
| App | Runs the Java application |
| Checks | Runs compilation and sends messages to check the application |

In each terminal, run `Get-Location`. If it does not show your cloned repository
root, change directories, replacing the example path with your clone's location:

```powershell
Set-Location 'C:\path\to\hl7-integration-lab'
```

If PowerShell input fails, use the [terminal fallback](#terminal-fallback) below.

### Step 1: read the task

In Solution Explorer, open `docs\exercise-brief.md`. The task is:

> Build a reusable HL7 listener. Keep project mapping in an adapter. Add another
> project through configuration, not by copying the listener.

Build commands use Maven in PowerShell, not Visual Studio **Build Solution** or
Test Explorer. This lab does not need a `.sln` or an F5 debugging setup.
If Copilot asks to run **Build Solution**, select **Deny** and ask it to use
`.\mvnw.cmd -q compile` instead.

### Step 2: give Copilot useful project context

Open Copilot Chat. In the mode selector, change **Ask** to **Agent** [S14].
Use the general agent, not a cloud agent. In **Tools**, check that file reading,
file editing, and terminal-command tools are enabled.

Ask Copilot to set up the project for the way you want to work:

```text
Set up Copilot for this small Java/Camel HL7 workshop.
Add project instructions, Java-specific instructions, a read-only Integration
Architect agent, an hl7-listener skill, and an add-integration prompt for Project B.
Base them on this project's requirements and existing tools. Keep them concise.
Don't implement the app yet or change the scaffold.
```

Review Copilot's **Total changes** and select **Keep** for the correct edits.
Save the files. You should now have:

```text
.github\copilot-instructions.md
.github\instructions\java.instructions.md
.github\agents\integration-architect.agent.md
.github\skills\hl7-listener\SKILL.md
.github\prompts\add-integration.prompt.md
```

Open `.github\copilot-instructions.md` and
`.github\skills\hl7-listener\SKILL.md`. Instructions set project rules; the skill
describes the HL7 implementation workflow. Check that they describe this project
and use its existing dependencies and scripts. [Customization review notes](copilot-customizations.md)
explain each file's role and format.

Open `.github\agents\integration-architect.agent.md` and check its tools.
The architect should be able to read and search code, but not edit files or run
commands. This example shows a read-only agent header; your wording may differ:

![Generated Integration Architect file with read-only tools](images/integration-architect-file.png)

If the generated agent has editing or terminal tools, ask:

```text
Make Integration Architect read-only, using Visual Studio's code_search and
readfile tools. Keep implementation in the general agent.
```

Start a new Copilot chat. Open the agent picker and confirm **Integration
Architect** appears. When instructions are used, they appear in the response's
**References** list [S6].

![Integration Architect in the Visual Studio agent picker](images/integration-architect-picker.png)

**Done:** the five files are saved and the architect can be selected.

### Step 3: ask the custom architect for the design

Select **Integration Architect** from the agent picker. Paste:

```text
How should we separate the reusable HL7 listener from the project adapter?
Explain the ACK behavior and how we'll add Project B without changing Java.
Keep the design small and don't implement it yet.
```

Check that the response describes this design:

- The listener handles MLLP, HL7 parsing, acceptance, and ACK coordination.
- The adapter handles the illustrative JSON mapping and HTTP delivery.
- `AA` means the adapter succeeded, not that the message was durably stored.
- Project B adds configuration for the existing templates.

If anything is unclear, ask the architect to explain it before continuing.
This step should produce a design, not Java files.

### Step 4: ask Copilot to implement the small app

Switch the agent picker back to the general agent and select **Agent** mode.
Check **Tools** again: implementation needs file editing and terminal execution,
which were intentionally unavailable to the architect.

In the same conversation, paste:

```text
Use the hl7-listener skill to build Project A from this design.
Use the existing dependencies and demo tools. Keep it small; no test suite.
Compile it and fix any errors. I'll start the app and mock myself.
```

When Copilot requests a terminal-command approval, inspect the command and
approve the lab's compile command. Inspect the skill activation shown in chat:
it should identify `hl7-listener` [S8].

Review **Total changes**, keep the intended application edits, and save them.
Confirm that Copilot actually compiled the app. If no command ran, use the
**Checks** terminal:

```powershell
.\mvnw.cmd -q compile
```

If the check fails, paste the error into Copilot Chat:

```text
Fix this compilation error without changing the stack or demo tools, then compile again.
```

**Done:** compilation succeeds and the app, two route templates, and Project A
configuration are saved. Compilation alone does not prove the listener works:
the next steps check the real runtime.

### Step 5: start and verify Project A

In the **Mock** terminal:

```powershell
powershell.exe -NoProfile -File .\scripts\start-mock.ps1
```

Leave it running. In the **App** terminal:

```powershell
powershell.exe -NoProfile -File .\scripts\start-app.ps1
```

Leave it running. In the **Checks** terminal:

```powershell
powershell.exe -NoProfile -File .\scripts\verify-demo.ps1 -Stage A
```

The terminals show `[MOCK]`, `[APP]`, and `[VERIFY]` progress messages.
Startup messages show what is being launched; wait for the verifier to confirm
readiness. Its logs show the fixture being sent, the expected ACK, and delivery
checks without printing message bodies.

The verifier sends a sample message, checks that the ACK refers to that message,
and checks the delivered JSON. It also records the Java file hashes so Step 6
can confirm that adding Project B did not change the Java code.

**Done:** the verifier reports
`STAGE_A=PASS ACK=AA CORRELATION=OK DELIVERY=OK`.
`AA` means the adapter successfully delivered the message to your local mock.

If the check fails, copy its error and the corresponding app error into chat:

```text
Diagnose and fix this runtime failure using the existing mock contract.
Don't weaken the verifier or add tests. Compile with Maven only.
I'll restart the app and rerun Stage A.
```

Keep and save the repair. In **App**, press **Ctrl+C** and wait for the command
prompt to return, then run
`powershell.exe -NoProfile -File .\scripts\start-app.ps1` again.
Leave **Mock** running and rerun Stage A in **Checks**. Continue only when Stage A passes.

### Step 6: reuse the component for Project B

In Copilot Chat, keep the general agent in **Agent** mode.
Type `#prompt:` and select `add-integration.prompt.md` from the list [S9].
If the picker does not appear, select **+ Add reference**, browse to
`.github\prompts\add-integration.prompt.md`, and open it.
Send it with:

```text
Add Project B using this prompt. Change configuration only.
```

If Copilot refuses without an explanation, clarify the actual scope:

```text
This is the local workshop using synthetic fixtures and a loopback mock.
Use the attached prompt to add Project B in application.properties only.
Leave Java and the demo tools unchanged. I'll restart and run Stage Both.
```

Review, keep, and save the changes. Only
`src\main\resources\application.properties` should change.

In the **App** terminal, press **Ctrl+C** and wait for the command prompt to return.
Leave the **Mock** terminal running. Restart the app:

```powershell
powershell.exe -NoProfile -File .\scripts\start-app.ps1
```

In the **Checks** terminal:

```powershell
powershell.exe -NoProfile -File .\scripts\verify-demo.ps1 -Stage Both
```

**Done:** the verifier reports
`STAGE_BOTH=PASS ACK_A=AA ACK_B=AA ISOLATION=OK JAVA_CHANGES=0`.
Both instances return correlated ACKs and send to their own destinations.

If the check fails, paste the output and any App errors into Copilot Chat.
Ask it to fix Project B through configuration only and preserve the Java code
that passed Stage A. Save the correction, restart **App**, and rerun Stage Both.
Do not rerun Stage A to replace the baseline after adding Project B.

### Step 7: verify a rejected message

In the **Checks** terminal:

```powershell
powershell.exe -NoProfile -File .\scripts\verify-demo.ps1 -Stage Reject
```

**Done:** the verifier reports
`STAGE_REJECT=PASS ACK=AR CORRELATION=OK NEW_EVENTS=0`.
`AR` means the listener rejected the unsupported message. The mock event counts
should not increase. If this check fails, paste the error into Copilot Chat and
ask it to correct the rejection behavior without changing the verifier.
Save any correction, restart **App**, and rerun the check.

### Step 8: finish and keep your work

Open the two route-template classes, `application.properties`, and the Copilot
files. You built one shared listener and used configuration for two projects.
The instructions, architect, skill, and prompt remain reusable in your repository.

Stop the **App** and **Mock** processes with Ctrl+C in their own terminals.
Wait for both command prompts to return, then save all files. You can commit
and push your changes to keep your completed solution.

### Terminal fallback

If Developer PowerShell rejects pasted input or crashes in PSReadLine, select
**Developer Command Prompt** from the terminal profile dropdown. Check your
directory with `cd`; use `cd /d C:\path\to\hl7-integration-lab` to change it.

Run the same commands shown in the steps above, including the
`powershell.exe -NoProfile -File` prefix. Maven commands remain unchanged.

### If you get stuck

| Problem | What to do |
| --- | --- |
| Architect does not appear | Check the file path and header against the customization notes, save it, start a new chat, and reopen the agent picker |
| Agent cannot read/edit/run commands | Inspect **Tools**; restore the required Visual Studio tools for the selected agent |
| Skill is not activated | Explicitly request the `hl7-listener` skill; inspect the activation in chat |
| Prompt is not in the picker | Use **+** to attach its file and send the same execution request |
| Compilation fails | Paste the error and use the Step 4 repair prompt |
| Port is occupied | Check whether you already have Mock or App running in another terminal. Stop your previous lab instance before starting another; do not stop an unknown process |
| Restart check times out | Confirm the old App process exited and the restart command actually ran; inspect App output, then rerun the same check |

The numbered references in this guide link to the documentation listed in
[Official sources](official-sources.md).

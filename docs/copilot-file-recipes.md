# Copilot file recipes

Visual Studio supports repository-wide instructions, file-targeted instructions,
custom agents, skills, and prompt files, with different activation behavior
[S6-S9]. This lab uses each for a distinct purpose.

Use Visual Studio's Copilot Chat **Agent** mode for file creation and
implementation. Switch to the custom architect for design, then manually back
to the general agent. Do not use VS Code tool names or handoff frontmatter.
Create files through Copilot, not an Insiders-only skills-creation panel.

### File 1: `.github\copilot-instructions.md`

```markdown
# HL7 Integration Lab

Read docs\exercise-brief.md and docs\acceptance-criteria.md before application work.
Use the Java 21 and Camel Main stack pinned in pom.xml. Do not change dependency
versions, add a framework, or introduce cloud services.

Keep the hl7-listener route template independent of project mappings and HTTP
destinations. Invoke a configured adapter URI. Use a separate demo-http-adapter
route template for the illustrative local JSON mapping and delivery.

Instantiate projects with Camel Main route-template properties. Do not hardcode
Project A or B in Java. Bind listeners to loopback for this exercise.

Use HAPI parsing and the existing fixtures. Treat the parsed message as internal;
never serialize the full HAPI object as the downstream JSON payload.

Use only synthetic data. Log listener ID, message ID, type, and safe outcome
metadata, never raw HL7, patient fields, or exception text containing payloads.

Follow the documented AA/AE/AR contract. Successful ACK means synchronous adapter
success, not durable intake. Preserve ACK correlation and negative outcomes.
No asynchronous handoff, broad success fallback, or retry policy in this lab.

Do not weaken assertions, change fixtures, or change support tools merely to make
the implementation pass. Report any genuine scaffold defect before altering it.

Keep this workshop small. Do not generate JUnit tests, add test frameworks, or
build production infrastructure. Compile with .\mvnw.cmd -q compile.
The participant proves behavior with the existing verify-demo.ps1 stages.
Report failures and fix the root cause within the agreed scope.
```

### File 2: `.github\instructions\java.instructions.md`

```markdown
---
description: Keep the HL7 workshop Java implementation small and reusable.
applyTo: "src/main/**/*.java"
---
Use the pinned Java/Camel dependencies. Keep only the classes needed for the app,
two route templates, envelope processing, and the small JSON DTO.
Keep project IDs, ports, and destinations in application.properties, not Java.
Use bounded HTTP deadlines and preserve ACK exchange properties.
Do not log raw messages or patient fields.
Do not create automated test classes or extra abstractions for this workshop.
```

Glob patterns use their standard forward-slash syntax; filesystem commands in
this Windows runbook use backslashes.

### File 3: `.github\agents\integration-architect.agent.md`

```markdown
---
name: Integration Architect
description: Design the reusable HL7 listener boundary and its acceptance contract.
tools: ["code_search", "readfile"]
---
You are the integration architect for this lab.
Read the exercise brief, acceptance criteria, protocol notes, and pinned stack.
Do not edit files or execute terminal commands.

Return a concise design with:
1. Shared listener responsibilities and project-adapter responsibilities.
2. The two route-template contracts and the internal envelope.
3. The AA/AE/AR behavior and the exact meaning of successful acknowledgment.
4. The three existing demo checks that prove delivery, reuse, and rejection.
5. Deferred production concerns.

Use Camel's native template configuration. Do not add a framework, persistence,
runtime LLM, or real Dynamics API. Distinguish parsing from application policy.
Explain how Project B can be added without changing Java.
Keep the response short enough for a two-minute human review.
```

The tools use Visual Studio's documented names [S7]. Verify them in Copilot's
**Tools** panel on the tested build. The architect has no editing or terminal
tool. The implementation step uses the general agent with file editing and
terminal execution enabled.

### File 4: `.github\skills\hl7-listener\SKILL.md`

```markdown
---
name: hl7-listener
description: Implement and run this lab's small reusable Camel HL7 v2 MLLP listener, correlated ACKs, project adapter boundary, and configuration-only reuse.
---
# Reusable HL7 listener workflow

Read the repository exercise brief, protocol notes, and acceptance criteria.
Use the pinned POM, existing scripts, and synthetic fixtures.

1. Inspect the scaffold and approved component contract.
2. Implement Camel Main discovery and the hl7-listener route template.
3. Parse with HAPI; require MSH-10 and the documented demo fields.
4. Apply configured message-type acceptance and create the internal envelope.
5. Invoke the configured direct adapter synchronously.
6. Implement the separate demo-http-adapter template and its small JSON DTO.
   Allowlist outbound HTTP headers without clearing ACK exchange properties.
7. Control generated ACKs with the documented Camel MLLP exchange property.
   Keep the original MSH-10 available for the consumer's ACK correlation.
8. Do not allow a handled HTTP or mapping failure to become an AA.
9. Do not generate test classes or introduce a test framework.
10. Run .\mvnw.cmd -q compile and fix compilation failures.
11. Explain the run commands and the three existing demo checks.

Use the prepared send_hl7.py and mock_destination.py support resources; inspect
their documented interfaces before calling them. They are not the application.
Do not rewrite transport framing or disable HL7 validation wholesale.
The prepared demo verifier checks real MLLP ACKs and destination JSON.

For reuse, append listener and adapter template instances to application.properties.
Do not duplicate the listener Java or introduce Project B Java conditionals.
Restart the app after configuration changes; this lab does not promise hot reload.
```

The skill references the existing repository documentation and support resources.
It need not duplicate scripts into its folder. Visual Studio shows an activated
skill in chat; verify that `hl7-listener` is applied during implementation [S8].
Do not require the Insiders-only Skills panel to complete the exercise.

### File 5: `.github\prompts\add-integration.prompt.md`

```markdown
Use the hl7-listener skill.
Read the exercise brief and inspect the current route-template configuration.
Add Project B on 127.0.0.1:2576, accepting ADT^A01, using direct:project-b and
the local mock destination http://127.0.0.1:8081/projects/project-b/events.

Change only src\main\resources\application.properties.
If the Java implementation cannot support this, stop and identify the design
defect rather than disguising it with project-specific code.

Do not change the listener, adapter Java, fixtures, or verification scripts.
Show the configuration diff. Tell me to stop and restart the app.
Do not run verification or restart processes yourself; I will run Stage Both.
Do not claim both projects work until the participant runs Stage Both.
```

Use a plain Markdown prompt body rather than unverified platform-specific
frontmatter. Invoke it through Visual Studio's `#prompt:` picker, or the `+`
context picker, as documented [S9]. Slash invocation is an optional convenience,
not a required step.

Do not embed a model name in these files. Use the organizer-tested model
available to the group and keep each participant's session choice stable.

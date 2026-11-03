# What the Copilot customizations do

These are review notes, not files to copy. Ask Copilot to create customizations
for this project, then inspect whether they help with the work. Different wording
is expected; identical output is not the goal.

| File | Purpose | What to check |
| --- | --- | --- |
| `.github\copilot-instructions.md` | Shared project rules | Uses the existing stack, keeps listener and mapping separate, stays small |
| `.github\instructions\java.instructions.md` | Java-specific guidance | Targets `src/main/**/*.java`; no project-specific listener code or generated tests |
| `.github\agents\integration-architect.agent.md` | Read-only design review | Named Integration Architect; reads files without editing or running commands |
| `.github\skills\hl7-listener\SKILL.md` | Reusable implementation workflow | Named hl7-listener; covers parsing, ACKs, adapter boundary, compilation, and demo checks |
| `.github\prompts\add-integration.prompt.md` | Repeatable Project B request | Adds configuration only, preserves Java, explains restart and Stage Both |

Use the short prompts in the [participant guide](participant-guide.md).
The exercise brief describes the integration requirement; it is not a hidden
solution or prewritten customization. Copilot should inspect the project and
turn its needs into useful instructions.

## Review before using them

Keep the files concise and avoid repeating the whole brief in every file.
No new framework, production infrastructure, test suite, or dependency changes
are needed. The supplied scripts already prove the live workshop scenario.

Visual Studio custom agents use YAML front matter with a description and a tools
list. For the read-only architect, Visual Studio documents `code_search` and
`readfile`; do not accept VS Code tool names or editing/terminal tools. A skill
needs a name and a description that explains when it applies. File-targeted
instructions need an `applyTo` glob. The saved Project B prompt can be plain
Markdown. See sources S6-S9 in [Official sources](official-sources.md).

Review the Project B prompt's concrete configuration:
loopback port 2576, ADT^A01, `direct:project-b`, and
`http://127.0.0.1:8081/projects/project-b/events`. It should change only
`src\main\resources\application.properties`, then tell the participant to restart
the app and run Stage Both. It must not report a runtime pass before that check.

If something is missing, use a short follow-up describing the problem, such as:

> Make the architect read-only using Visual Studio's code_search and readfile
> tools. Keep implementation work in the general agent.

Review meaning, not exact phrasing. Do not copy a canonical answer just to make
everyone's files identical.

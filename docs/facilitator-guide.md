# Facilitator guide

Keep the workshop to the running component and its configuration-only reuse.
Do not ask participants to generate JUnit tests or production infrastructure.
Use Maven compile followed by the three supplied end-to-end demo checks.

Use the participant guide's natural-language prompts. Let Copilot create useful
customizations from the project context; do not make participants copy canonical
instruction files. Review behavior and scope rather than identical wording.

Build in your own fresh template copy using section 6, exactly as participants do.
Announce the step number and pause at minutes 6, 21, 28, and 31 to check the
group's milestone. Use the same prompts and checks; do not substitute private
automation on your machine.

Participants who finish early should inspect their instructions, agent, skill,
and template configuration rather than expand the app. Participants who are
blocked use the repair prompt or the shared checkpoint path. Provide helper
support for individual environment failures instead of stopping everyone's flow.

| Trigger | Action |
| --- | --- |
| Copilot customizations are not ready by minute 6 | Offer the customization checkpoint to affected participants; disclose the switch |
| Architect proposes a much larger system | Ask it to follow the exercise brief with only Camel Main and the two documented templates |
| Application is not compiling by minute 21 | Use the Step 4 repair prompt if time permits; otherwise offer the Project A checkpoint |
| Dependencies begin downloading slowly | Use the rehearsed, already-warmed checkpoint environment; do not add tooling live |
| Project B requires Java modifications | Treat this as a design failure; do not call it configuration-only reuse |
| A port is occupied | Identify the owning process; stop it only if it is a known lab process, otherwise use a rehearsed alternative configuration |
| Prompt picker differs | Use the Visual Studio **+** context picker to attach the prompt file |
| Skill was not loaded | Explicitly request it and inspect tool activity; do not claim invocation based on discovery |
| HTTP delivery fails but ACK is AA | Stop the success claim and fix ACK handling; this is a central contract defect |

If a reference checkpoint is used, the final result can still show a running
component and reuse. It no longer demonstrates that all application code was
generated live. Be explicit about that distinction.

The 35-minute lab begins after every participant has completed setup. It includes
guided independent implementation, not installation or account provisioning.
Pilot the exact guide with developers first. If the group cannot reach the
milestones, simplify the application scope before the event or provide additional
lab time; do not claim that a presenter-only run proves the group timing.

# Environment

Use Windows and open the **repository root as a folder** in Visual Studio.
This is Java/Maven, not a `.sln` lab: do not use F5, Build Solution, or Test Explorer.

## Before opening the timed lab

Install Visual Studio 2026 18.5 or later, Git, a Java 21 **JDK** (including `javac`),
and Python 3.10 or later from their official distributors. Sign in to Visual
Studio with your own GitHub account and Copilot access. Installation and account
setup are preparation, not part of the 35 minutes.

Set `JAVA_HOME` to your JDK directory (not its `bin` directory), and put that
JDK's `bin` and Python on PATH. Open a new PowerShell terminal after changing
environment variables. Confirm `java -version`, `javac -version`, and
`python --version`.

The author machine currently has Visual Studio **18.11.12328.437**, Temurin
**25.0.5**, and Python **3.14.10**. Camel 4.22 supports Java 25 as well as 21;
the POM still compiles for Java **release 21**. Preflight accepts either JDK.
Do not describe a JDK 25 rehearsal as a Java 21 runtime test; the rehearsal
record identifies which was actually used.

In Visual Studio, enable repository custom instructions under
**Tools > Options > All Settings > GitHub > Copilot > Copilot Chat**.
Use **View > Terminal**, select PowerShell, and run:

```powershell
Get-Location
.\scripts\warmup.ps1
.\scripts\preflight.ps1
```

Warmup resolves dependencies/plugins but creates no application or active
Copilot files. First-time downloads need network access to Maven Central.
Later compile/test/plugin execution can still download transitive plugin
dependencies; complete organizer rehearsal before promising an offline lab.

If scripts are blocked by organizational policy, use your organization's approved
script-signing or execution-policy process. Do **not** disable policy globally or
require a blanket bypass. If PATH resolves a Store alias instead of Python,
install/configure the real Python command before the session.

## Frozen build versions

| Item | Version |
| --- | --- |
| Java bytecode/API release | 21 |
| Camel BOM and Camel modules | 4.22.2 LTS |
| HAPI base and v2.5 structures | 2.6.0 (resolved from camel-hl7 4.22.2 POM) |
| SLF4J simple (only binding) | 2.0.17 |
| Maven / Wrapper plugin | 3.9.11 / 3.3.4, only-script distribution |
| Compiler | 3.14.1 |
| Exec / Dependency / Resources | 3.6.2 / 3.8.1 / 3.3.1 |
| Jar / Clean / Install / Deploy | 3.4.2 / 3.4.1 / 3.1.4 / 3.1.4 |

The wrapper's Maven ZIP checksum is pinned in
`.mvn\wrapper\maven-wrapper.properties`. Do not change versions during the lab.

Prepare three terminal tabs: **Mock**, **App**, **Checks**. All must be at the
same repository root. Preflight requires loopback ports 2575, 2576, and 8081 free
and must run **before** starting processes. Never terminate an unknown port owner.

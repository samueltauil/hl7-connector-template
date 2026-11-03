$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$failures = [System.Collections.Generic.List[string]]::new()
foreach ($command in @('java', 'javac', 'python', 'git')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        $failures.Add("Install $command and open a new terminal so PATH is refreshed.")
    }
}
if (Get-Command java -ErrorAction SilentlyContinue) {
    $versionOutput = (& java -version 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0 -or $versionOutput -notmatch 'version "(21|25)\.') {
        $failures.Add('Use a Java 21 JDK (or the documented Java 25 rehearsal environment).')
    }
}
if (Get-Command javac -ErrorAction SilentlyContinue) {
    $compiler = (& javac -version 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0 -or $compiler -notmatch 'javac (21|25)\.') {
        $failures.Add('javac must be from a Java 21 or 25 JDK, not just a JRE.')
    }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
    if ($LASTEXITCODE -ne 0) { $failures.Add('Install Python 3.10 or later; disable Store aliases if necessary.') }
}
foreach ($file in @('mvnw.cmd', '.mvn\wrapper\maven-wrapper.properties',
    'fixtures\adt-a01-project-a.hl7', 'fixtures\adt-a01-project-b.hl7',
    'fixtures\adt-a08-unsupported.hl7', 'fixtures\adt-a01-missing-patient-reference.hl7')) {
    if (-not (Test-Path $file -PathType Leaf)) { $failures.Add("Missing $file. Open a complete template copy.") }
}
foreach ($port in @(2575, 2576, 8081)) {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $port)
    try { $listener.Start() }
    catch [System.Net.Sockets.SocketException] { $failures.Add("Port $port is occupied. Identify its owner; do not stop an unknown process.") }
    finally { $listener.Stop() }
}
if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Host "PREFLIGHT_FAILED: $_" -ForegroundColor Red }
    exit 1
}
& .\mvnw.cmd -v
if ($LASTEXITCODE -ne 0) { Write-Error 'Maven Wrapper failed. Check JAVA_HOME, network, and .mvn files.'; exit 1 }
Write-Host 'PREFLIGHT=PASS PORTS=FREE'

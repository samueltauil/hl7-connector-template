$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "[APP] Working directory: $((Get-Location).Path)"
Write-Host '[APP] Compiling and launching the Java application with Maven...'
Write-Host '[APP] Leave this terminal running. Use the Checks terminal to verify readiness and delivery.'
& .\mvnw.cmd -q compile exec:java
$exitCode = $LASTEXITCODE
if ($exitCode -eq 0) { Write-Host '[APP] Application stopped (exit code 0).' }
else { Write-Host "[APP] Application exited with code $exitCode. Check the errors above." -ForegroundColor Red }
exit $exitCode

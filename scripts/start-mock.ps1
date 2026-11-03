$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "[MOCK] Working directory: $((Get-Location).Path)"
Write-Host '[MOCK] Starting the local HTTP destination at http://127.0.0.1:8081...'
Write-Host '[MOCK] Leave this terminal running. Use the Checks terminal to verify readiness and delivery.'
& python -u .\scripts\mock_destination.py
$exitCode = $LASTEXITCODE
if ($exitCode -eq 0) { Write-Host '[MOCK] Mock stopped (exit code 0).' }
else { Write-Host "[MOCK] Mock exited with code $exitCode. Check the errors above." -ForegroundColor Red }
exit $exitCode

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\mvnw.cmd -B -q validate dependency:go-offline
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'WARMUP=PASS APPLICATION_FILES_CREATED=0'

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& python -u .\scripts\mock_destination.py
exit $LASTEXITCODE

param([Parameter(Mandatory = $true)][ValidateSet('A', 'Both', 'Reject')][string]$Stage)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$mock = 'http://127.0.0.1:8081'
$baselineFile = '.lab-runtime\java-baseline.json'

function Wait-Ready([int[]]$Ports) {
    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    do {
        $ready = $false
        try {
            $health = Invoke-RestMethod "$mock/health" -TimeoutSec 2
            $ready = $health.ready -eq $true -and $health.service -eq 'non-durable-local-mock'
            foreach ($port in $Ports) {
                $client = [System.Net.Sockets.TcpClient]::new()
                try {
                    $task = $client.ConnectAsync('127.0.0.1', $port)
                    if (-not $task.Wait(500) -or -not $client.Connected) { $ready = $false }
                }
                finally { $client.Dispose() }
            }
        }
        catch [System.Net.Http.HttpRequestException] { $ready = $false }
        catch [System.Net.WebException] { $ready = $false }
        catch [System.AggregateException] { $ready = $false }
        if ($ready) { return }
        Start-Sleep -Milliseconds 150
    } while ([DateTime]::UtcNow -lt $deadline)
    throw 'Readiness deadline reached. Start Mock and App in their own terminals; inspect their errors.'
}

function Get-Events([string]$Project) {
    $result = Invoke-RestMethod "$mock/projects/$Project/events" -TimeoutSec 3
    return @($result)
}

function Get-JavaFingerprint {
    $files = @(Get-ChildItem .\src -Filter *.java -Recurse -File | Sort-Object FullName)
    if ($files.Count -eq 0) { throw 'No application/test Java files were found.' }
    $root = (Get-Location).Path + '\'
    return @($files | ForEach-Object {
        [PSCustomObject]@{ path = $_.FullName.Substring($root.Length); hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash }
    })
}

function Send-Fixture([int]$Port, [string]$File, [string]$Expected) {
    & python .\scripts\send_hl7.py --host 127.0.0.1 --port $Port --file ".\fixtures\$File" --expect $Expected --timeout 5
    if ($LASTEXITCODE -ne 0) { throw "Wire verification failed for $File on port $Port." }
}

function Assert-Delivery($Before, $After, [string]$Id, [string]$Source, [string]$Patient) {
    if (@($After).Count -ne @($Before).Count + 1) { throw "Expected exactly one new event for $Id." }
    $event = @($After)[-1]
    if ($event.externalMessageId -ne $Id -or $event.eventType -ne 'ADT^A01' -or
        $event.sourceApplication -ne $Source -or $event.patientReference -ne $Patient -or
        @($event.PSObject.Properties).Count -ne 4) {
        throw "Destination content mismatch for $Id."
    }
}

try {
    $ports = @(2575)
    if ($Stage -eq 'Both') { $ports += 2576 }
    Wait-Ready $ports
    if ($Stage -eq 'Both') {
        if (-not (Test-Path $baselineFile)) { throw 'Missing Stage A baseline. Run Stage A before adding Project B.' }
        $baseline = Get-Content $baselineFile -Raw | ConvertFrom-Json
        $current = @(Get-JavaFingerprint)
        $difference = @(Compare-Object $baseline $current -Property path, hash)
        if ($difference.Count -ne 0) { throw 'Java sources changed after Stage A. Configuration-only reuse was not demonstrated.' }
    }
    $aBefore = @(Get-Events 'project-a')
    $bBefore = @(Get-Events 'project-b')
    if ($Stage -eq 'Reject') {
        Send-Fixture 2575 'adt-a08-unsupported.hl7' 'AR'
        if (@(Get-Events 'project-a').Count -ne $aBefore.Count -or
            @(Get-Events 'project-b').Count -ne $bBefore.Count) { throw 'Rejected message created downstream events.' }
        Write-Host 'STAGE_REJECT=PASS ACK=AR CORRELATION=OK NEW_EVENTS=0'
        exit 0
    }
    Send-Fixture 2575 'adt-a01-project-a.hl7' 'AA'
    $aAfter = @(Get-Events 'project-a')
    Assert-Delivery $aBefore $aAfter 'DEMO-A-001' 'LAB-A' 'SYNTH-A-100'
    if (@(Get-Events 'project-b').Count -ne $bBefore.Count) { throw 'Project A event leaked into Project B.' }
    if ($Stage -eq 'A') {
        New-Item .lab-runtime -ItemType Directory -Force | Out-Null
        ConvertTo-Json -InputObject @(Get-JavaFingerprint) | Set-Content $baselineFile -Encoding UTF8
        Write-Host 'STAGE_A=PASS ACK=AA CORRELATION=OK DELIVERY=OK'
    }
    else {
        Send-Fixture 2576 'adt-a01-project-b.hl7' 'AA'
        $bAfter = @(Get-Events 'project-b')
        Assert-Delivery $bBefore $bAfter 'DEMO-B-001' 'LAB-B' 'SYNTH-B-200'
        if (@(Get-Events 'project-a').Count -ne $aAfter.Count) { throw 'Project B event leaked into Project A.' }
        Write-Host 'STAGE_BOTH=PASS ACK_A=AA ACK_B=AA ISOLATION=OK JAVA_CHANGES=0'
    }
}
catch {
    Write-Host "VERIFY_FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

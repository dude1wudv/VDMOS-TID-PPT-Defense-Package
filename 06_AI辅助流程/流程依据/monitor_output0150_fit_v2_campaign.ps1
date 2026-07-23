[CmdletBinding()]
param(
    [string] $CampaignId = 'trench_tid_output0150_fit_v2_20260718T033500Z',
    [ValidateRange(15, 3600)] [int] $PollSeconds = 45,
    [switch] $Once
)

# Read-only observer and proposal writer. It never starts a dispatcher, retries,
# recovery, parameter generator, or deck creation process.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$LocalRoot = Join-Path $RepoRoot "local_runtime\tcad_runs\$CampaignId"
$Dispatcher = Join-Path $PSScriptRoot 'run_output0150_fit_v2_dispatcher.ps1'
$SvisualRunner = Join-Path $PSScriptRoot 'run_svisual_extract.ps1'
$Validator = Join-Path $PSScriptRoot 'validate_output0150_fit_v2.py'
$Scorer = Join-Path $PSScriptRoot 'score_output0150_fit_v2.py'
$CampaignConfigPath = Join-Path $RepoRoot 'simulation\config\output0150_fit_v2\campaign.json'
$RefinementManifestPath = Join-Path $RepoRoot 'simulation\config\output0150_fit_v2\refinement_manifest.json'
$MonitorDir = Join-Path $LocalRoot 'monitor'
$EventLog = Join-Path $MonitorDir 'monitor_events.ndjson'
$StatusLog = Join-Path $MonitorDir 'dispatcher_status.log'
$DispatcherLog = Join-Path $MonitorDir 'refinement_dispatcher.log'
$script:RefillPid = $null
New-Item -ItemType Directory -Force -Path $MonitorDir | Out-Null

function Read-Json([string] $Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    try { Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop } catch { return $null }
}
function Write-Json([string] $Path, [object] $Value) {
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    $text = ($Value | ConvertTo-Json -Depth 32) + "`n"
    [IO.File]::WriteAllText([IO.Path]::GetFullPath($Path), $text, (New-Object Text.UTF8Encoding($false)))
}
function Log-Event([string] $Kind, [object] $Payload) {
    $record = [ordered]@{ timestamp_utc = [DateTime]::UtcNow.ToString('o'); kind = $Kind; payload = $Payload }
    ($record | ConvertTo-Json -Depth 32 -Compress) | Add-Content -LiteralPath $EventLog -Encoding UTF8
}
function Invoke-Child([string] $File, [string[]] $Arguments, [string] $LogPath) {
    & $File @Arguments *>&1 | Tee-Object -FilePath $LogPath -Append | Out-Host
    [int]$LASTEXITCODE
}
function Get-StagePrefix([string] $CandidateId, [string] $Stage, [int] $Attempt) {
    if ($Stage -eq 'feedback_screen_d00_recovery_a1') {
        return "v2_${CandidateId}_feedback_screen_recovery_a${Attempt}"
    }
    "v2_${CandidateId}_feedback_screen_a${Attempt}"
}
function Get-ExpectedCaseId([string] $CandidateId, [string] $Stage, [int] $Attempt) {
    Get-StagePrefix $CandidateId $Stage $Attempt
}
function Get-PhysicalMap {
    $map = @{}
    $base = Read-Json $CampaignConfigPath
    if ($null -ne $base -and $null -ne $base.PSObject.Properties['candidates']) {
        foreach ($item in @($base.candidates)) {
            if ($null -eq $item) { continue }
            $map[[string]$item.candidate_id] = [pscustomobject]@{
                candidate_id = [string]$item.candidate_id
                epi_h_um = [double]$item.epi_h_um
                epi_doping_cm3 = [double]$item.epi_doping_cm3
            }
        }
    }
    $ref = Read-Json $RefinementManifestPath
    if ($null -ne $ref -and $null -ne $ref.PSObject.Properties['candidates']) {
        foreach ($item in @($ref.candidates)) {
            if ($null -eq $item) { continue }
            $map[[string]$item.candidate_id] = [pscustomobject]@{
                candidate_id = [string]$item.candidate_id
                epi_h_um = [double]$item.epi_h_um
                epi_doping_cm3 = [double]$item.epi_doping_cm3
            }
        }
    }
    $map
}
function Find-RunInfo([object] $Item) {
    $root = Join-Path $LocalRoot "$($Item.candidate_id)\sdevice_runs"
    if (-not (Test-Path -LiteralPath $root -PathType Container)) { return $null }
    $prefix = Get-StagePrefix ([string]$Item.candidate_id) ([string]$Item.stage) ([int]$Item.attempt)
    $expectedCase = Get-ExpectedCaseId ([string]$Item.candidate_id) ([string]$Item.stage) ([int]$Item.attempt)
    $dirs = @(Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "$prefix*" } | Sort-Object LastWriteTimeUtc -Descending)
    foreach ($dir in $dirs) {
        $manifestPath = Join-Path $dir.FullName 'run_manifest.json'
        $manifest = Read-Json $manifestPath
        if ($null -eq $manifest -or [string]$manifest.case_id -ne $expectedCase) { continue }
        return [pscustomobject]@{ dir = $dir.FullName; manifest = $manifest; manifest_path = $manifestPath }
    }
    $null
}
function Get-InputHash([object] $Manifest, [string] $Suffix) {
    @($Manifest.inputs | Where-Object { [string]$_.relative_path -like "*$Suffix" } |
        ForEach-Object { [string]$_.sha256 }) | Select-Object -First 1
}
function Get-InputLeaf([object] $Manifest, [string] $Suffix) {
    @($Manifest.inputs | Where-Object { [string]$_.relative_path -like "*$Suffix" } |
        ForEach-Object { Split-Path -Leaf ([string]$_.relative_path) }) | Select-Object -First 1
}
function Ensure-RunEvidence([object] $Item, [object] $RunInfo) {
    $manifest = $RunInfo.manifest
    if ([string]$manifest.lifecycle -notin @('SUCCEEDED','FAILED','TIMED_OUT')) { return $false }
    $runDir = [string]$RunInfo.dir
    $validationPath = Join-Path $runDir 'validation_v2.json'
    $existing = Read-Json $validationPath
    if ($null -ne $existing -and [string]$existing.run_id -eq [string]$manifest.run_id) {
        $scorePath = Join-Path $runDir 'score_v2.json'
        if ($null -eq (Read-Json $scorePath)) {
            $csv = Get-ChildItem -LiteralPath $runDir -Filter "$($manifest.case_id).csv" -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($null -ne $csv) {
                $scoreArgs = @($Scorer,'--csv',$csv.FullName,'--validation',$validationPath,'--output',$scorePath)
                Invoke-Child 'python' $scoreArgs (Join-Path $runDir 'score_v2.stdout.log') | Out-Null
            }
        }
        return $true
    }
    $pltLeaf = @($manifest.artifacts | Where-Object { [string]$_.relative_path -like 'artifacts/IdVd_*.plt' } |
        ForEach-Object { Split-Path -Leaf ([string]$_.relative_path) }) | Select-Object -First 1
    if ([string]::IsNullOrWhiteSpace($pltLeaf)) {
        # A failed run without a PLT is retained as numerical no-data only after
        # the runner manifest proves lease/lifecycle completion; no fake CSV.
        Log-Event 'missing_plt' ([ordered]@{ candidate_id=$Item.candidate_id; stage=$Item.stage; run_id=$manifest.run_id })
        return $false
    }
    $remoteRoot = [string]$manifest.remote_run_dir
    $remotePlt = "$remoteRoot/inputs/$pltLeaf"
    $safeRun = ([string]$manifest.run_id) -replace '[^A-Za-z0-9_.-]', '_'
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
    $indexPath = Join-Path $runDir 'svisual_index.json'
    $index = [ordered]@{
        schema_version = 'trench_tid_output0150_fit_v2_svisual_index/v1'
        campaign_id = $CampaignId
        display_required = 'DISPLAY=:0.0'
        records = @([ordered]@{
            case_id = [string]$manifest.case_id
            kind = [string]$Item.stage
            dose_krad_si = 0
            plt = $remotePlt
            x_variable = 'drain InnerVoltage'
            run_id = [string]$manifest.run_id
            formal_eligible = $false
        })
    }
    Write-Json $indexPath $index
    $svisualDir = Join-Path $runDir 'svisual'
    $remoteWork = "/home/tcad/codex_runs/$CampaignId/svisual_extract/${safeRun}_$stamp"
    $extractLog = Join-Path $runDir 'svisual_extract.log'
    $extractArgs = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$SvisualRunner,'-IndexPath',$indexPath,'-LocalOutputDir',$svisualDir,'-RemoteWorkDir',$remoteWork)
    $extractCode = Invoke-Child 'powershell.exe' $extractArgs $extractLog
    if ($extractCode -ne 0) {
        Log-Event 'svisual_failed' ([ordered]@{ candidate_id=$Item.candidate_id; stage=$Item.stage; run_id=$manifest.run_id; exit_code=$extractCode })
        return $false
    }
    $csv = Get-ChildItem -LiteralPath $svisualDir -Filter "$($manifest.case_id).csv" -File -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -eq $csv) {
        Log-Event 'svisual_no_csv' ([ordered]@{ candidate_id=$Item.candidate_id; stage=$Item.stage; run_id=$manifest.run_id })
        return $false
    }
    $deckHash = Get-InputHash $manifest '.cmd'
    $meshHash = Get-InputHash $manifest '.tdr'
    $validateArgs = @($Validator,'--run-dir',$runDir,'--csv',$csv.FullName,'--deck-hash',$deckHash,'--mesh-hash',$meshHash,'--output',$validationPath)
    $validateCode = Invoke-Child 'python' $validateArgs (Join-Path $runDir 'validation_v2.stdout.log')
    if ($validateCode -ne 0) {
        Log-Event 'validation_failed' ([ordered]@{ candidate_id=$Item.candidate_id; stage=$Item.stage; run_id=$manifest.run_id; exit_code=$validateCode })
        return $false
    }
    $scorePath = Join-Path $runDir 'score_v2.json'
    $scoreArgs = @($Scorer,'--csv',$csv.FullName,'--validation',$validationPath,'--output',$scorePath)
    $scoreCode = Invoke-Child 'python' $scoreArgs (Join-Path $runDir 'score_v2.stdout.log')
    Log-Event 'evidence_scored' ([ordered]@{ candidate_id=$Item.candidate_id; stage=$Item.stage; run_id=$manifest.run_id; score_exit_code=$scoreCode; classification=(Read-Json $validationPath).classification })
    $scoreCode -eq 0
}
function Refresh-Dispatcher {
    $args = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$Dispatcher,'-Mode','Status','-CampaignId',$CampaignId)
    Invoke-Child 'powershell.exe' $args $StatusLog | Out-Null
}
function Refill-Dispatcher {
    Log-Event 'automatic_dispatch_disabled' ([ordered]@{ action='refill_dispatcher'; reason='human_decision_record_required' })
}
function Get-State { Read-Json (Join-Path $LocalRoot 'dispatcher\status_manifest.json') }
function Get-TerminalEvidence([object] $State) {
    $results = @()
    foreach ($item in @($State.work_items | Where-Object { $_.stage -in @('feedback_screen_d00','feedback_screen_d00_recovery_a1') })) {
        $run = Find-RunInfo $item
        if ($null -eq $run) { continue }
        if (Ensure-RunEvidence $item $run) {
            $validationPath = Join-Path $run.dir 'validation_v2.json'
            $validation = Read-Json $validationPath
            if ($null -ne $validation) {
                $results += [pscustomobject]@{ item=$item; run=$run; validation=$validation; score=(Read-Json (Join-Path $run.dir 'score_v2.json')) }
            }
        }
    }
    $results
}
function Select-TrendCenter([object[]] $Evidence, [hashtable] $Physical) {
    $eligible = @()
    foreach ($entry in $Evidence) {
        $v = $entry.validation
        if ([string]$v.classification -notin @('TREND_CANDIDATE','STRONG_TREND','PARTIAL_TREND_CANDIDATE')) { continue }
        if ($null -eq $Physical[[string]$entry.item.candidate_id]) { continue }
        $f = $v.trend_features
        $rise = if ($null -eq $f.log10_abs_id_rise) { -1e9 } else { [double]$f.log10_abs_id_rise }
        $points = if ($null -eq $f.points_80_120v) { 0 } else { [int]$f.points_80_120v }
        $mono = if ($null -eq $f.monotonic_non_decreasing_fraction) { 0.0 } else { [double]$f.monotonic_non_decreasing_fraction }
        $endpoint = if ($null -eq $v.partial_endpoint_v) { 1e9 } else { [double]$v.partial_endpoint_v }
        $eligible += [pscustomobject]@{
            candidate_id = [string]$entry.item.candidate_id
            classification = [string]$v.classification
            strong = ([string]$v.classification -eq 'STRONG_TREND')
            rise = $rise
            points = $points
            mono = $mono
            endpoint = $endpoint
            h_um = [double]$Physical[[string]$entry.item.candidate_id].epi_h_um
            nd_cm3 = [double]$Physical[[string]$entry.item.candidate_id].epi_doping_cm3
            run_id = [string]$entry.validation.run_id
        }
    }
    @($eligible | Sort-Object @{Expression='strong';Descending=$true}, @{Expression='rise';Descending=$true}, @{Expression='points';Descending=$true}, @{Expression={ [Math]::Abs($_.endpoint - 100.0) };Descending=$false})
}
function Has-ActiveWork([object] $State) {
    @($State.work_items | Where-Object { $_.status -in @('READY','CLAIMED','RUNNING','FINALIZATION_PENDING') }).Count -gt 0
}
function Start-NewDispatcher {
    Log-Event 'automatic_dispatch_disabled' ([ordered]@{ action='new_dispatcher'; reason='human_decision_record_required' })
    $null
}
function Args-String([string[]] $Values) {
    ($Values | ForEach-Object {
        $text = [string]$_
        if ($text -match '[\s"]') { '"' + $text.Replace('"','\"') + '"' } else { $text }
    }) -join ' '
}
function Maybe-GenerateRefinement([object] $State, [object[]] $Evidence, [hashtable] $Physical) {
    # Compatibility name only: selection is observational and no work is made.
    Log-Event 'automatic_decision_disabled' ([ordered]@{
        action='selection_refinement_retry_or_dispatch'
        campaign_id=$CampaignId
        evidence_count=@($Evidence).Count
        required_next_state='HUMAN_APPROVAL_PENDING'
    })
    $false
}

Log-Event 'monitor_started' ([ordered]@{ campaign_id=$CampaignId; poll_seconds=$PollSeconds; pid=$PID })
while ($true) {
    try {
        Log-Event 'step_begin' ([ordered]@{ step='refresh_dispatcher' })
        Refresh-Dispatcher
        Log-Event 'step_end' ([ordered]@{ step='refresh_dispatcher' })
        Log-Event 'step_begin' ([ordered]@{ step='refill_dispatcher' })
        Refill-Dispatcher
        Log-Event 'step_end' ([ordered]@{ step='refill_dispatcher' })
        Log-Event 'step_begin' ([ordered]@{ step='get_state' })
        $state = Get-State
        Log-Event 'step_end' ([ordered]@{ step='get_state'; available=($null -ne $state) })
        if ($null -eq $state) { throw 'status manifest unavailable' }
        Log-Event 'step_begin' ([ordered]@{ step='terminal_evidence' })
        $evidence = @(Get-TerminalEvidence $state)
        Log-Event 'step_end' ([ordered]@{ step='terminal_evidence'; count=$evidence.Count })
        $physical = Get-PhysicalMap
        Log-Event 'poll' ([ordered]@{
            active=@($state.work_items | Where-Object { $_.status -in @('CLAIMED','RUNNING','FINALIZATION_PENDING') }).Count
            ready=@($state.work_items | Where-Object { $_.status -eq 'READY' }).Count
            evidence_count=$evidence.Count
            lease_count=$state.scheduling.managed_lease_count
            classifications=@($evidence | ForEach-Object { "$($_.item.candidate_id):$($_.validation.classification)" })
        })
        Log-Event 'step_begin' ([ordered]@{ step='maybe_generate' })
        $generated = Maybe-GenerateRefinement $state $evidence $physical
        Log-Event 'step_end' ([ordered]@{ step='maybe_generate'; generated=[bool]$generated })
        if ($Once) { break }
    } catch {
        Log-Event 'monitor_error' ([ordered]@{ message=$_.Exception.Message; type=$_.Exception.GetType().FullName })
        if ($Once) { break }
    }
    Start-Sleep -Seconds $PollSeconds
}
Log-Event 'monitor_stopped' ([ordered]@{ once=[bool]$Once })
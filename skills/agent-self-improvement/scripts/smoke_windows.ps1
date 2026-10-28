param(
    [Parameter(Mandatory = $true)][string]$Project,
    [Parameter(Mandatory = $true)][string]$Repo,
    [ValidateSet("codex", "opencode")][string]$Engine = "codex",
    [string]$RunId,
    [switch]$RunLive
)

$ErrorActionPreference = "Stop"
$scriptRoot = $PSScriptRoot
$projectPath = (Resolve-Path -LiteralPath $Project).Path
$repoPath = (Resolve-Path -LiteralPath $Repo).Path

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.12+ must be available on PATH"
}

Write-Host "Running offline self-improvement regression tests..."
& python -m unittest discover -s $scriptRoot -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) {
    throw "Self-improvement tests failed (exit $LASTEXITCODE)"
}

Write-Host "Inspecting project-local collection status..."
& python (Join-Path $scriptRoot "learning.py") status --project $projectPath
if ($LASTEXITCODE -ne 0) {
    throw "Learning store status failed"
}

if ($RunLive) {
    if (-not $RunId) {
        throw "-RunId from a completed begin diagnosis is required for live project analysis"
    }
    if (-not (Get-Command $Engine -ErrorAction SilentlyContinue)) {
        throw "$Engine CLI is not on PATH; install and authenticate it before a live run"
    }
    Write-Host "Running model-backed analysis; this can send stored experience to the configured provider..."
    & python (Join-Path $scriptRoot "learning_cycle.py") propose --run $RunId --repo $repoPath --project $projectPath --engine $Engine
    if ($LASTEXITCODE -ne 0) {
        throw "Live learning cycle failed (exit $LASTEXITCODE)"
    }
} else {
    Write-Host "Offline tests passed. Add -RunLive only after reviewing the recorded data and provider permissions."
}

Write-Host "Finished. No skill changes were applied."

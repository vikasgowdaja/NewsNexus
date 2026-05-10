$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Missing .venv interpreter at $pythonExe. Create the virtual environment and install requirements first."
}

& $pythonExe (Join-Path $root "run_all.py") @args
exit $LASTEXITCODE
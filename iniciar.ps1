param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Stop existing processes
Get-Process -Name uvicorn -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq "" } | Stop-Process -Force

if (-not $FrontendOnly) {
    Write-Host "[1/2] Iniciando backend (puerto 8765)..." -ForegroundColor Green
    Start-Process -WindowStyle Normal -FilePath "uvicorn" -ArgumentList "app.main:app --host 0.0.0.0 --port 8765" -WorkingDirectory (Join-Path $root "backend")
}

if (-not $BackendOnly) {
    Start-Sleep -Seconds 3
    Write-Host "[2/2] Iniciando frontend (puerto 5173)..." -ForegroundColor Green
    Start-Process -WindowStyle Normal -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory (Join-Path $root "frontend")
}

Write-Host ""
Write-Host "Sistema iniciado. Abre http://localhost:5173" -ForegroundColor Cyan
Write-Host "Cierra las ventanas de Backend y Frontend para detener." -ForegroundColor Yellow

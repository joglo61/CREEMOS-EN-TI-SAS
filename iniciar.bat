@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo  CREEMOS EN TI SAS - Inicio del Sistema
echo ========================================
echo.

REM Kill existing processes
taskkill /f /im uvicorn.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

echo [1/2] Iniciando backend (puerto 8765)...
ver >nul
start "Backend" cmd /c "cd /d "%~dp0backend" && uvicorn app.main:app --host 0.0.0.0 --port 8765"
if %errorlevel% neq 0 (
    echo ERROR: No se pudo iniciar el backend.
    pause
    exit /b 1
)

timeout /t 3 /nobreak >nul

echo [2/2] Iniciando frontend (puerto 5173)...
start "Frontend" cmd /c "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Sistema iniciado. Abre http://localhost:5173 en tu navegador.
echo Cierra las ventanas de Backend y Frontend para detener el sistema.
echo.
pause

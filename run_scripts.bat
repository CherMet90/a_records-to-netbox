@echo off

rem Run the PowerShell script
powershell.exe -ExecutionPolicy Bypass -File ".\export.ps1"

rem Check if the PowerShell script executed successfully
if %ERRORLEVEL% == 0 (
    rem Run the Python script only if the PowerShell script was successful
    python.exe ".\main.py"
) else (
    echo PowerShell script failed with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
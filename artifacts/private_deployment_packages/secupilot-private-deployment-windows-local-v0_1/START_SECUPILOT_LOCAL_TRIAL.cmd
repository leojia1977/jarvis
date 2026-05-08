@echo off
setlocal
echo SecuPilot local offline trial entry
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\START_CUSTOMER_TRIAL.ps1"
if errorlevel 1 (
  echo LOCAL_TRIAL_ENTRY_HOLD
  pause
  exit /b 1
)
echo LOCAL_TRIAL_ENTRY_READY
pause

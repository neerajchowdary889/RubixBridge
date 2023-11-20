@echo off
setlocal enabledelayedexpansion
set "logfile=C:\Users\ubuntu\cronlog\rubixstartup.log"

rem Determine the location of the batch script
for %%F in ("%~dp0") do set "script_dir=%%~dpF"

rem Navigate to the rubixgoplatform\linux directory
set "rubix_dir=!script_dir!\..\rubix\rubixgoplatform\linux"

echo Starting sessions >> !logfile!

set "base_port=20000"
set "base_grpc_port=10500"

rem Change directory to rubixgoplatform directory
cd /d "!rubix_dir!" || exit /b 1

for /l %%i in (1,1,7) do (
  set /a "port=base_port + %%i - 1"
  set /a "grpc_port=base_grpc_port + %%i - 1"
  start "Node%%i" cmd /c ".\rubixgoplatform.exe run -p Node%%i -n %%i -s -port !port! -testNet -grpcPort !grpc_port!"
  echo Started session for Node%%i, port: !port!, grpcPort: !grpc_port! >> !logfile!
)

echo All sessions started >> !logfile!

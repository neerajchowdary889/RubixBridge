@echo off
setlocal enabledelayedexpansion
set "logfile=rubixstartup.log"

rem Determine the location of the batch script
for %%F in ("%~dp0") do set "script_dir=%%~dpF"

rem Navigate to the rubixgoplatform\linux directory
set "rubix_dir=C:\Users\saishibu\Documents\rubixgoplatform-SC\rubixgoplatform-develop\windows"

echo Starting sessions >> !logfile!

set "base_port=20000"
set "base_grpc_port=10500"

rem Change directory to rubixgoplatform directory
cd /d "!rubix_dir!" || exit /b 1

for /l %%i in (0,1,6) do (
  set /a "port=base_port + %%i"
  set /a "grpc_port=base_grpc_port + %%i"
  start "Node%%i" cmd /c ".\rubixgoplatform.exe run -p Node%%i -n %%i -s -port !port! -testNet -grpcPort !grpc_port!"
  timeout /t 10 
  echo Started session for Node%%i, port: !port!, grpcPort: !grpc_port! >> !logfile!
)

echo All sessions started >> !logfile!

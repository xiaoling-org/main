@echo off
echo Installing Amazon Corretto 17 JDK...
echo Please run this as Administrator if prompted

msiexec /i "C:\Users\czp\Downloads\amazon-corretto-17.msi" /quiet /norestart

if %ERRORLEVEL% EQU 0 (
    echo JDK installation started successfully
) else (
    echo JDK installation failed with error code %ERRORLEVEL%
)

pause
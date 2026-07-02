@echo off
REM Build dist\xkoranate\xkoranate.exe
cd /d "%~dp0"
.venv\Scripts\pyinstaller.exe --noconfirm xkoranate.spec || exit /b 1
echo Built: %cd%\dist\xkoranate\xkoranate.exe

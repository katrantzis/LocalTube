@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 desktop\localtube_app.py
  goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
  python desktop\localtube_app.py
  goto :end
)
echo Python 3 wurde nicht gefunden.
echo Installiere Python 3 von https://www.python.org/downloads/windows/
echo Aktiviere beim Installieren die Option "Add Python to PATH".
pause
:end
endlocal

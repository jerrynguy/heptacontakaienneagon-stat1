@echo off
REM Build Heptacontakaienneagon Stat into a single .exe (needs Python 3.10+ on Windows)
cd /d "%~dp0"
python -m pip install --upgrade -r requirements-build.txt || goto :err
python -m PyInstaller --noconfirm --clean hstat.spec || goto :err
echo.
echo Done: dist\HeptacontakaienneagonStat.exe
pause
exit /b 0
:err
echo Build failed - see messages above.
pause
exit /b 1

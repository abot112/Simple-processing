@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
cd /d "%~dp0"

rem Conda env AD - edit path if your env moves
set "CONDA_ENV_AD=C:\Users\MASHIRO\.conda\envs\AD"
set "PYTHON_AD=%CONDA_ENV_AD%\python.exe"

if not exist "%PYTHON_AD%" (
    echo [ERROR] Python not found:
    echo   %PYTHON_AD%
    echo Edit CONDA_ENV_AD in start.bat if needed.
    pause
    exit /b 1
)

echo Starting ImageTool with conda env AD...
"%PYTHON_AD%" "src\main.py"
set "EXITCODE=%ERRORLEVEL%"
if not "%EXITCODE%"=="0" (
    echo.
    echo [ERROR] Program exited with code %EXITCODE%.
)
echo.
pause
endlocal

@echo off
REM Error Recovery & Graceful Degradation System
REM Quick commands for managing error recovery

echo ============================================
echo  ERROR RECOVERY SYSTEM
echo ============================================
echo.

if "%1"=="" goto menu

if "%1"=="status" goto status
if "%1"=="test" goto test
if "%1"=="monitor" goto monitor
goto menu

:menu
echo Choose an action:
echo.
echo   1. Check System Status
echo   2. Test Error Handling
echo   3. Start Health Monitoring
echo   4. View Error Log
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto test
if "%choice%"=="3" goto monitor
if "%choice%"=="4" goto view_log
if "%choice%"=="5" goto end
goto menu

:status
echo.
echo Checking Error Recovery System Status...
echo.
python error_recovery.py --status
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:test
echo.
echo Running Error Recovery Tests...
echo.
python error_recovery.py --test
echo.
echo Tests complete!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:monitor
echo.
echo Starting Health Monitoring...
echo.
echo Monitoring will check all services every 30 seconds
echo Press Ctrl+C to stop monitoring
echo.
pause
python error_recovery.py --monitor
goto menu

:view_log
echo.
echo Opening Error Log...
echo.
if exist "logs\error_recovery\error_log.json" (
    start notepad "logs\error_recovery\error_log.json"
    echo Opened: logs\error_recovery\error_log.json
) else (
    echo No error log found. Errors will be logged when they occur.
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
echo.
echo Exiting...
echo.

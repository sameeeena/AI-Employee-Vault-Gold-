@echo off
REM Comprehensive Audit Logging System
REM Quick commands for audit logging

echo ============================================
echo  AUDIT LOGGING SYSTEM
echo ============================================
echo.

if "%1"=="" goto menu

if "%1"=="status" goto status
if "%1"=="log" goto log
if "%1"=="report" goto report
if "%1"=="monitor" goto monitor
goto menu

:menu
echo Choose an action:
echo.
echo   1. Check Audit Status
echo   2. Log Test Events
echo   3. Generate Audit Report
echo   4. Start Real-time Monitoring
echo   5. View Audit Logs
echo   6. Exit
echo.
set /p choice="Enter choice (1-6): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto log
if "%choice%"=="3" goto report
if "%choice%"=="4" goto monitor
if "%choice%"=="5" goto view_logs
if "%choice%"=="6" goto end
goto menu

:status
echo.
echo Checking Audit Log Status...
echo.
python audit_logger.py --status
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:log
echo.
echo Logging Test Events...
echo.
python audit_logger.py --log
echo.
echo Events logged successfully!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:report
echo.
echo Generating Audit Report...
echo.
python audit_logger.py --report
echo.
echo Report generated! Check audit_reports folder.
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:monitor
echo.
echo Starting Real-time Monitoring...
echo.
echo Monitoring will alert on critical events
echo Press Ctrl+C to stop monitoring
echo.
pause
python audit_logger.py --monitor
goto menu

:view_logs
echo.
echo Opening Audit Logs Folder...
echo.
if exist "audit_logs" (
    explorer audit_logs
    echo Opened: audit_logs
) else (
    echo Audit logs folder not found. Log some events first.
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
echo.
echo Exiting...
echo.

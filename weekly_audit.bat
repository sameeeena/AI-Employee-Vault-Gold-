@echo off
REM Weekly Business & Accounting Audit System
REM Quick commands for running audits and generating CEO briefings

echo ============================================
echo  WEEKLY AUDIT SYSTEM
echo ============================================
echo.

if "%1"=="" goto menu

if "%1"=="run" goto run_audit
if "%1"=="generate" goto generate
if "%1"=="schedule" goto schedule
goto menu

:menu
echo Choose an action:
echo.
echo   1. Run Weekly Audit (Manual)
echo   2. Generate CEO Briefing
echo   3. Start Weekly Scheduler
echo   4. View Latest Briefing
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto run_audit
if "%choice%"=="2" goto generate
if "%choice%"=="3" goto schedule
if "%choice%"=="4" goto view
if "%choice%"=="5" goto end
goto menu

:run_audit
echo.
echo Running Weekly Audit...
echo.
python weekly_audit.py
echo.
echo Audit complete! Check the 'audits' folder for reports.
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:generate
echo.
echo Generating CEO Briefing from existing audit data...
echo.
python weekly_audit.py --generate
echo.
echo Briefing generated! Check the 'audits' folder.
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:schedule
echo.
echo Starting Weekly Audit Scheduler...
echo.
echo Scheduler will run every Monday at 9:00 AM
echo Press Ctrl+C to stop the scheduler
echo.
pause
python weekly_audit.py --schedule
goto menu

:view
echo.
echo Opening latest CEO Briefing...
echo.
if exist "audits" (
    for %%f in (audits\ceo_briefing_*.md) do (
        set "latest=%%f"
    )
    if defined latest (
        start notepad "%latest%"
        echo Opened: %latest%
    ) else (
        echo No briefing files found. Run an audit first.
    )
) else (
    echo Audits folder not found. Run an audit first.
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
echo.
echo Exiting...
echo.

@echo off
REM Ralph Wiggum Loop - Autonomous Task Completion
REM Quick commands for Ralph Loop

echo ============================================
echo  RALPH WIGGUM LOOP
echo ============================================
echo.

if "%1"=="" goto menu

if "%1"=="demo" goto demo
if "%1"=="status" goto status
if "%1"=="task" goto task
goto menu

:menu
echo Choose an action:
echo.
echo   1. Run Demo
echo   2. Check Status
echo   3. Execute Task
echo   4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto demo
if "%choice%"=="2" goto status
if "%choice%"=="3" goto task
if "%choice%"=="4" goto end
goto menu

:demo
echo.
echo Running Ralph Loop Demo...
echo.
python ralph_loop.py --demo
echo.
echo Demo complete!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:status
echo.
echo Checking Ralph Loop Status...
echo.
python ralph_loop.py --status
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:task
echo.
echo Execute Custom Task
echo.
set /p goal="Enter task goal: "
set /p priority="Enter priority (low/medium/high/critical) [medium]: "
if "%priority%"=="" set priority=medium

echo.
echo Executing task...
echo.
python ralph_loop.py --task "%goal%" --priority %priority%
echo.
echo Task execution complete!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
echo.
echo Exiting...
echo.

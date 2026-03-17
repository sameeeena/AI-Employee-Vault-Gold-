@echo off
REM MCP Server Management Batch File
REM Quick commands to manage all MCP servers

echo ============================================
echo  MCP SERVER MANAGEMENT
echo ============================================
echo.

if "%1"=="" goto menu

if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="status" goto status
if "%1"=="health" goto health
goto menu

:menu
echo Choose an action:
echo.
echo   1. Start all MCP servers
echo   2. Stop all MCP servers
echo   3. Check status
echo   4. Check health
echo   5. Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto status
if "%choice%"=="4" goto health
if "%choice%"=="5" goto end
goto menu

:start
echo.
echo Starting all MCP servers...
echo.
python mcp_orchestrator.py start
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:stop
echo.
echo Stopping all MCP servers...
echo.
python mcp_orchestrator.py stop
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:status
echo.
echo Checking MCP server status...
echo.
python mcp_orchestrator.py status
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:health
echo.
echo Checking MCP server health...
echo.
python mcp_orchestrator.py health
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:end
echo.
echo Exiting...
echo.

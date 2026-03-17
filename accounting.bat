@echo off
REM ===========================================
REM Accounting MCP Server Command
REM ===========================================
REM Usage: accounting [start|stop|status|test]
REM ===========================================

if "%1"=="start" (
    echo Starting Accounting MCP Server...
    echo Connecting to Odoo at http://localhost:8069
    start_accounting.bat
    goto :end
)

if "%1"=="stop" (
    echo Stopping Accounting MCP Server...
    taskkill /F /FI "WINDOWTITLE eq Accounting*" /IM python.exe 2>nul
    echo Server stopped.
    goto :end
)

if "%1"=="test" (
    echo Testing Accounting MCP Server endpoints...
    echo.
    echo 1. Testing Health Check...
    curl http://localhost:8000/health
    echo.
    echo.
    echo 2. Running full test suite...
    python test_accounting.py
    goto :end
)

if "%1"=="status" (
    echo Checking Accounting MCP Server status...
    curl http://localhost:8000/health
    echo.
    echo.
    echo Checking Odoo modules...
    python check_odoo_modules.py
    goto :end
)

echo.
echo ===========================================
echo   ACCOUNTING MCP SERVER
echo ===========================================
echo.
echo Usage: accounting [command]
echo.
echo Commands:
echo   start   - Start the Accounting MCP Server
echo   stop    - Stop the server
echo   test    - Test API endpoints
echo   status  - Check server health + Odoo modules
echo.
echo Quick Start:
echo   1. accounting start
echo   2. Install Invoicing app in Odoo
echo   3. accounting test
echo.
echo Documentation:
echo   ACCOUNTING_QUICKSTART.md
echo   ODOO_ACCOUNTING_SETUP.md
echo.
echo ===========================================

:end

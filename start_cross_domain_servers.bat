@echo off
REM ================================================================
REM Cross-Domain MCP Servers Starter
REM Starts all 4 MCP servers for full cross-domain integration:
REM - Accounting MCP Server (port 8001)
REM - Social Media MCP Server (port 8002)
REM - Personal MCP Server (port 8003)
REM - Business MCP Server (port 8004)
REM ================================================================

echo ================================================================
echo   CROSS-DOMAIN MCP SERVERS STARTER
echo   Full Integration: Personal + Business + Accounting + Social
echo ================================================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting MCP Servers...
echo.

REM Start Accounting MCP Server
echo [1/4] Starting Accounting MCP Server (port 8001)...
start "Accounting MCP" python accounting_mcp_server.py
timeout /t 2 /nobreak >nul

REM Start Social Media MCP Server
echo [2/4] Starting Social Media MCP Server (port 8002)...
start "Social MCP" python social_mcp_server.py
timeout /t 2 /nobreak >nul

REM Start Personal MCP Server
echo [3/4] Starting Personal MCP Server (port 8003)...
start "Personal MCP" python personal_mcp_server.py
timeout /t 2 /nobreak >nul

REM Start Business MCP Server
echo [4/4] Starting Business MCP Server (port 8004)...
start "Business MCP" python business_mcp_server.py
timeout /t 2 /nobreak >nul

echo.
echo ================================================================
echo   All MCP Servers Starting...
echo ================================================================
echo.
echo   Server                  Port    Status
echo   ----------------------  ------  --------
echo   Accounting MCP          8001    Starting...
echo   Social Media MCP        8002    Starting...
echo   Personal MCP            8003    Starting...
echo   Business MCP            8004    Starting...
echo.
echo   Wait a few seconds for servers to initialize.
echo   Run: python mcp_server_manager.py health
echo   to check server status.
echo.
echo ================================================================

REM Wait and check health
timeout /t 5 /nobreak >nul
echo.
echo Checking server health...
python mcp_server_manager.py health

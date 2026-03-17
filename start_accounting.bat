@echo off
REM ===========================================
REM Start Accounting MCP Server
REM ===========================================

REM Set Odoo credentials
set ODOO_URL=http://localhost:8069
set ODOO_DB=odoo_db
set ODOO_USERNAME=sameena02134@gmail.com
set ODOO_PASSWORD=admin

REM Start the server
echo Starting Accounting MCP Server...
echo Odoo URL: %ODOO_URL%
echo Odoo DB: %ODOO_DB%
echo Odoo Username: %ODOO_USERNAME%
echo.
python accounting_mcp_server.py

@echo off
REM ============================================================================
REM  Facebook & Instagram Integration - Quick Start
REM ============================================================================
REM  This script helps you get started with the Facebook/Instagram integration
REM ============================================================================

echo.
echo ============================================================================
echo  FACEBOOK & INSTAGRAM INTEGRATION - QUICK START
echo ============================================================================
echo.

:MENU
echo.
echo Please select an option:
echo.
echo  1. Run Test Suite (Mock Mode)
echo  2. Start Social MCP Server
echo  3. View API Documentation (in browser)
echo  4. Edit Configuration (.env file)
echo  5. View Integration Guide
echo  6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto RUN_TESTS
if "%choice%"=="2" goto START_SERVER
if "%choice%"=="3" goto OPEN_DOCS
if "%choice%"=="4" goto EDIT_CONFIG
if "%choice%"=="5" goto VIEW_GUIDE
if "%choice%"=="6" goto EXIT

echo Invalid choice. Please try again.
goto MENU

:RUN_TESTS
echo.
echo Running Test Suite...
echo.
python test_facebook_instagram.py
echo.
pause
goto MENU

:START_SERVER
echo.
echo Starting Social MCP Server...
echo.
echo Server will start on http://localhost:8002
echo Press Ctrl+C to stop the server
echo.
python social_mcp_server_v2.py
goto MENU

:OPEN_DOCS
echo.
echo Opening API documentation in your default browser...
start http://localhost:8002/docs
echo.
echo Note: Make sure the server is running first!
echo.
pause
goto MENU

:EDIT_CONFIG
echo.
echo Opening .env file for editing...
notepad .env
echo.
echo Remember to set:
echo   - FACEBOOK_PAGE_ID
echo   - FACEBOOK_ACCESS_TOKEN
echo   - INSTAGRAM_USER_ID
echo   - INSTAGRAM_ACCESS_TOKEN
echo   - SOCIAL_MOCK_MODE=false (for live posting)
echo.
pause
goto MENU

:VIEW_GUIDE
echo.
echo Opening Integration Guide...
start FACEBOOK_INSTAGRAM_INTEGRATION.md
echo.
pause
goto MENU

:EXIT
echo.
echo Thank you for using Facebook & Instagram Integration!
echo.
exit /b

@echo off
REM ===========================================
REM Social Media MCP Server Command
REM ===========================================
REM Usage: social [start|stop|status|test|post-fb|post-ig]
REM ===========================================

if "%1"=="start" (
    echo ===========================================
    echo   Starting Social MCP Server
    echo ===========================================
    echo.
    echo Platforms: Facebook, Instagram, Twitter
    echo Server: http://localhost:8001
    echo.
    python social_mcp_server.py
    goto :end
)

if "%1"=="stop" (
    echo Stopping Social MCP Server...
    taskkill /F /FI "WINDOWTITLE eq social*" /IM python.exe 2>nul
    echo Server stopped.
    goto :end
)

if "%1"=="test" (
    echo ===========================================
    echo   Testing Social MCP Server
    echo ===========================================
    echo.
    echo 1. Health Check...
    curl http://localhost:8001/health
    echo.
    echo.
    echo 2. Check credentials in .env...
    findstr /i "FACEBOOK" .env
    findstr /i "INSTAGRAM" .env
    echo.
    echo.
    echo ===========================================
    echo   TEST COMMANDS
    echo ===========================================
    echo.
    echo Post to Facebook:
    echo curl -X POST http://localhost:8001/post_message -H "Content-Type: application/json" -d "{\"platform\": \"facebook\", \"message\": \"Test!\"}"
    echo.
    echo Post to Instagram:
    echo curl -X POST http://localhost:8001/post_message -H "Content-Type: application/json" -d "{\"platform\": \"instagram\", \"message\": \"Test!\", \"image_url\": \"https://example.com/img.jpg\"}"
    echo.
    goto :end
)

if "%1"=="status" (
    echo Checking Social MCP Server status...
    curl http://localhost:8001/health
    goto :end
)

if "%1"=="post-fb" (
    if "%2"=="" (
        echo Usage: social post-fb "Your message here"
        goto :end
    )
    echo Posting to Facebook...
    curl -X POST http://localhost:8001/post_message ^
      -H "Content-Type: application/json" ^
      -d "{\"platform\": \"facebook\", \"message\": \"%2\"}"
    goto :end
)

if "%1"=="post-ig" (
    if "%2"=="" (
        echo Usage: social post-ig "Your message here" "image_url"
        goto :end
    )
    if "%3"=="" (
        echo Error: Instagram requires an image URL
        echo Usage: social post-ig "Your message here" "https://example.com/image.jpg"
        goto :end
    )
    echo Posting to Instagram...
    curl -X POST http://localhost:8001/post_message ^
      -H "Content-Type: application/json" ^
      -d "{\"platform\": \"instagram\", \"message\": \"%2\", \"image_url\": \"%3\"}"
    goto :end
)

if "%1"=="summary" (
    if "%2"=="" (
        echo Usage: social summary "post_id"
        goto :end
    )
    echo Generating summary for post %2...
    curl -X POST http://localhost:8001/generate_post_summary ^
      -H "Content-Type: application/json" ^
      -d "{\"platform\": \"facebook\", \"post_id\": \"%2\"}"
    goto :end
)

echo.
echo ===========================================
echo   SOCIAL MEDIA MCP SERVER
echo ===========================================
echo.
echo Usage: social [command] [parameters]
echo.
echo Commands:
echo   start              - Start the Social MCP Server
echo   stop               - Stop the server
echo   status             - Check server health
echo   test               - Test API endpoints
echo   post-fb "message"  - Post to Facebook
echo   post-ig "msg" "url"- Post to Instagram (needs image)
echo   summary "post_id"  - Generate post summary
echo.
echo Examples:
echo   social start
echo   social post-fb "Hello from AI Employee!"
echo   social post-ig "Beautiful day!" "https://example.com/photo.jpg"
echo   social summary "12345_67890"
echo.
echo Documentation:
echo   SOCIAL_MEDIA_QUICKSTART.md - Quick setup
echo   SOCIAL_MEDIA_SETUP.md      - Full guide
echo.
echo ===========================================

:end

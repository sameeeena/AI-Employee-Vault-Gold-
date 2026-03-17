@echo off
REM ============================================
REM Facebook Auto-Post - Quick Start
REM ============================================

echo ============================================
echo   FACEBOOK AUTO-POST - QUICK START
echo ============================================
echo.

echo Select action:
echo   1. Post to Facebook NOW (immediate post)
echo   2. Setup auto-post schedules (recurring posts)
echo   3. Start auto-post scheduler (background service)
echo   4. Check scheduled posts
echo   5. Test Facebook connection (mock mode)
echo.

set /p choice="Your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Posting to Facebook now...
    python autopost_facebook.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Setting up auto-post schedules...
    python setup_autopost_schedules.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting auto-post scheduler in background...
    start python social_scheduler.py
    echo Scheduler started! Check logs\scheduled_posts_log.md for updates.
    pause
) else if "%choice%"=="4" (
    echo.
    echo Checking scheduled posts...
    python -c "import asyncio; from social_content_calendar import ContentCalendarManager; posts = asyncio.run(ContentCalendarManager().get_pending_posts()); print(f'\nFound {len(posts)} pending posts:'); [print(f'  - {p.scheduled_time}: {p.message[:50]}...') for p in posts]"
    pause
) else if "%choice%"=="5" (
    echo.
    echo Testing Facebook connection (mock mode)...
    python -c "import asyncio; from facebook_instagram_integration import FacebookInstagramIntegration; int = FacebookInstagramIntegration(mock_mode=True); result = asyncio.run(int.post_to_facebook('Test post from AI Employee Vault! #Test')); print('\nTest result:', result)"
    pause
) else (
    echo.
    echo Invalid choice. Please run again and select 1-5.
    pause
)

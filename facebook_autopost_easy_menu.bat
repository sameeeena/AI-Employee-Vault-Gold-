@echo off
REM ============================================
REM Facebook Auto-Post - Easy Menu
REM ============================================

:menu
cls
echo ============================================
echo   FACEBOOK AUTO-POST - EASY MENU
echo ============================================
echo.
echo Select an option:
echo.
echo   === IMMEDIATE POSTS ===
echo   1. Post Now (Show Templates)
echo   2. Post - Product Announcement (Template 1)
echo   3. Post - Business Tips (Template 2)
echo   4. Post - Motivational (Template 3)
echo   5. Post - Industry Insights (Template 4)
echo   6. Post - Customer Success (Template 5)
echo   7. Post - Feature Highlight (Template 6)
echo   8. Post - Educational (Template 7)
echo   9. Post - Special Offer (Template 8)
echo.
echo   === SCHEDULED POSTS ===
echo   10. Schedule Post for Specific Time
echo   11. Schedule Daily Recurring Post
echo   12. Schedule Weekly Recurring Post
echo   13. View All Scheduled Posts
echo.
echo   === OTHER OPTIONS ===
echo   14. Start Auto-Post Scheduler
echo   15. Test Facebook Connection (Mock Mode)
echo   16. View Documentation
echo   0. Exit
echo.
echo ============================================

set /p choice="Your choice (0-16): "

if "%choice%"=="1" goto post_show_templates
if "%choice%"=="2" goto post_template1
if "%choice%"=="3" goto post_template2
if "%choice%"=="4" goto post_template3
if "%choice%"=="5" goto post_template4
if "%choice%"=="6" goto post_template5
if "%choice%"=="7" goto post_template6
if "%choice%"=="8" goto post_template7
if "%choice%"=="9" goto post_template8
if "%choice%"=="10" goto schedule_specific
if "%choice%"=="11" goto schedule_daily
if "%choice%"=="12" goto schedule_weekly
if "%choice%"=="13" goto view_schedules
if "%choice%"=="14" goto start_scheduler
if "%choice%"=="15" goto test_connection
if "%choice%"=="16" goto view_docs
if "%choice%"=="0" goto exit

echo Invalid choice. Please try again.
timeout /t 2
goto menu

:post_show_templates
cls
echo ============================================
echo   POST TO FACEBOOK - SHOW TEMPLATES
echo ============================================
python facebook_autopost_now.py
pause
goto menu

:post_template1
cls
echo ============================================
echo   POSTING: Product Announcement
echo ============================================
python facebook_autopost_now.py --template 1
pause
goto menu

:post_template2
cls
echo ============================================
echo   POSTING: Business Tips
echo ============================================
python facebook_autopost_now.py --template 2
pause
goto menu

:post_template3
cls
echo ============================================
echo   POSTING: Motivational Post
echo ============================================
python facebook_autopost_now.py --template 3
pause
goto menu

:post_template4
cls
echo ============================================
echo   POSTING: Industry Insights
echo ============================================
python facebook_autopost_now.py --template 4
pause
goto menu

:post_template5
cls
echo ============================================
echo   POSTING: Customer Success
echo ============================================
python facebook_autopost_now.py --template 5
pause
goto menu

:post_template6
cls
echo ============================================
echo   POSTING: Feature Highlight
echo ============================================
python facebook_autopost_now.py --template 6
pause
goto menu

:post_template7
cls
echo ============================================
echo   POSTING: Educational Content
echo ============================================
python facebook_autopost_now.py --template 7
pause
goto menu

:post_template8
cls
echo ============================================
echo   POSTING: Special Offer
echo ============================================
python facebook_autopost_now.py --template 8
pause
goto menu

:schedule_specific
cls
echo ============================================
echo   SCHEDULE POST FOR SPECIFIC TIME
echo ============================================
echo.
set /p date="Enter date (YYYY-MM-DD): "
set /p time="Enter time (HH:MM): "
set /p template="Enter template ID (1-8): "
echo.
python facebook_autopost_schedule.py --date %date% --time %time% --template %template%
pause
goto menu

:schedule_daily
cls
echo ============================================
echo   SCHEDULE DAILY RECURRING POST
echo ============================================
echo.
set /p time="Enter time (HH:MM): "
set /p template="Enter template ID (1-8): "
echo.
python facebook_autopost_schedule.py --recurring daily --time %time% --template %template%
pause
goto menu

:schedule_weekly
cls
echo ============================================
echo   SCHEDULE WEEKLY RECURRING POST
echo ============================================
echo.
set /p time="Enter time (HH:MM): "
set /p template="Enter template ID (1-8): "
echo.
python facebook_autopost_schedule.py --recurring weekly --time %time% --template %template%
pause
goto menu

:view_schedules
cls
echo ============================================
echo   VIEW SCHEDULED POSTS
echo ============================================
python facebook_autopost_schedule.py --list
pause
goto menu

:start_scheduler
cls
echo ============================================
echo   START AUTO-POST SCHEDULER
echo ============================================
echo.
echo Starting scheduler in background...
echo Scheduler will automatically post at scheduled times.
echo.
echo To stop scheduler, close the Python process in Task Manager.
echo.
start python social_scheduler.py
echo Scheduler started!
pause
goto menu

:test_connection
cls
echo ============================================
echo   TEST FACEBOOK CONNECTION
echo ============================================
echo.
echo Testing in mock mode...
echo.
python -c "import asyncio; from facebook_instagram_integration import FacebookInstagramIntegration; int = FacebookInstagramIntegration(mock_mode=True); result = asyncio.run(int.post_to_facebook('Test post from AI Employee Vault! #Test')); print('\nTest result:', result)"
pause
goto menu

:view_docs
cls
echo ============================================
echo   DOCUMENTATION
echo ============================================
echo.
echo Opening documentation...
echo.
start FACEBOOK_AUTOPOST_QUICKSTART_URDU.md
pause
goto menu

:exit
cls
echo ============================================
echo   Thank you for using Facebook Auto-Post!
echo ============================================
timeout /t 2
exit

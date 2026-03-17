@echo off
echo ============================================
echo  FACEBOOK TOKEN GENERATOR - QUICK START
echo ============================================
echo.
echo Opening Facebook Graph API Explorer...
echo.
echo INSTRUCTIONS:
echo 1. Select your app from the dropdown
echo 2. Click "Get Token" -^> "Get Page Access Token"
echo 3. Select your Facebook Page (1496288429174042)
echo 4. Grant these permissions:
echo    - pages_manage_posts
echo    - pages_read_engagement
echo    - pages_show_list
echo 5. Copy the generated token
echo 6. Paste it in .env file (no quotes)
echo 7. Save and run: test_facebook_token.py
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

REM Open Graph API Explorer
start https://developers.facebook.com/tools/explorer/

echo.
echo Browser opened!
echo.
echo After getting the token, press any key to open .env file...
pause >nul

REM Open .env file
start notepad .env

echo.
echo ============================================
echo  Next steps:
echo  1. Paste token in .env (FACEBOOK_PAGE_ACCESS_TOKEN=...)
echo  2. Save .env file
echo  3. Run: python test_facebook_token.py
echo ============================================
echo.

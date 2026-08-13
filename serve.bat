@echo off
REM ho-yu.github.io 로컬 미리보기 서버 실행
REM 더블클릭하면 http://127.0.0.1:4000 에서 사이트를 볼 수 있습니다.
REM 종료하려면 이 창에서 Ctrl+C 를 누르세요.

cd /d "%~dp0"

echo Ruby / Bundler 확인 중...
where ruby >nul 2>nul
if errorlevel 1 (
    echo [오류] ruby 명령을 찾을 수 없습니다. Ruby 설치 후 새 터미널에서 다시 시도하세요.
    pause
    exit /b 1
)

echo.
echo Jekyll 서버를 시작합니다... ^(http://127.0.0.1:4000^)
echo.

bundle exec jekyll serve

pause

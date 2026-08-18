@echo off
chcp 65001 >nul
REM ho-yu.github.io 로컬 미리보기 서버 실행 (Windows)
REM 더블클릭 실행: serve.bat
REM 종료: 이 창에서 Ctrl+C

cd /d "%~dp0"

where ruby >nul 2>nul
if errorlevel 1 (
    echo [오류] ruby 명령을 찾을 수 없습니다. Ruby 설치 후 새 터미널에서 다시 시도하세요.
    echo   winget install RubyInstallerTeam.RubyWithDevKit.3.4
    pause
    exit /b 1
)

where bundle >nul 2>nul
if errorlevel 1 (
    echo Bundler 설치 중...
    call gem install bundler
)

echo 의존성 확인 중... ^(bundle install^)
call bundle install
if errorlevel 1 (
    echo [오류] bundle install 실패.
    pause
    exit /b 1
)

echo.
echo Jekyll 서버를 시작합니다... ^(http://127.0.0.1:4000^)
echo.

call bundle exec jekyll serve

pause

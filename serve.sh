#!/usr/bin/env bash
# ho-yu.github.io 로컬 미리보기 서버 실행 (macOS / Linux)
# 터미널 실행: ./serve.sh
# macOS 더블클릭 실행: serve.command
# 종료: 이 터미널에서 Ctrl+C

set -e
cd "$(dirname "$0")"

# macOS(Homebrew) keg-only Ruby 3.4를 쓰는 경우 PATH에 추가
if command -v brew >/dev/null 2>&1 && brew --prefix ruby@3.4 >/dev/null 2>&1; then
    export PATH="$(brew --prefix ruby@3.4)/bin:$PATH"
fi

if ! command -v ruby >/dev/null 2>&1; then
    echo "[오류] ruby 명령을 찾을 수 없습니다. Ruby 설치 후 다시 시도하세요."
    echo "  brew install ruby@3.4"
    exit 1
fi

if ! command -v bundle >/dev/null 2>&1; then
    echo "Bundler 설치 중..."
    gem install bundler
fi

echo "의존성 확인 중... (bundle install)"
bundle install

echo
echo "Jekyll 서버를 시작합니다... (http://127.0.0.1:4000)"
echo

bundle exec jekyll serve

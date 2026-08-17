#!/usr/bin/env bash
# macOS Finder에서 더블클릭하여 로컬 미리보기 서버를 실행한다.

script_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$script_dir" || exit 1

bash "$script_dir/serve.sh" "$@"
exit_code=$?

if [[ $exit_code -ne 0 && $exit_code -ne 130 && -t 0 ]]; then
  echo
  read -r -p "실행에 실패했습니다. Enter 키를 누르면 창이 닫힙니다." _
fi

exit "$exit_code"

#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
launcher="$repo_root/serve.command"

if [[ ! -x "$launcher" ]]; then
  echo "FAIL: serve.command is missing or not executable" >&2
  exit 1
fi

if [[ ! -x "$repo_root/serve.sh" ]]; then
  echo "FAIL: serve.sh is not executable" >&2
  exit 1
fi

bash -n "$launcher" "$repo_root/serve.sh"

test_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$test_dir"
}
trap cleanup EXIT

cp "$launcher" "$test_dir/serve.command"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'printf "cwd=%s\\narg=%s\\n" "$PWD" "${1:-}"' >"$test_dir/serve.sh"
chmod +x "$test_dir/serve.command" "$test_dir/serve.sh"

output="$("$test_dir/serve.command" launcher-check)"
expected="$(printf 'cwd=%s\narg=launcher-check' "$test_dir")"

if [[ "$output" != "$expected" ]]; then
  echo "FAIL: serve.command did not launch serve.sh from its own directory" >&2
  printf 'expected:\n%s\nactual:\n%s\n' "$expected" "$output" >&2
  exit 1
fi

echo "PASS: macOS double-click launcher delegates to serve.sh correctly"

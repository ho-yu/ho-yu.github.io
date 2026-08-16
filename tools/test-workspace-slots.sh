#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"

for slot_number in 01 02 03 04 05; do
  slot_path="$repo_root/workspace/draft-$slot_number.md"
  if [[ ! -f "$slot_path" ]]; then
    echo "FAIL: required workspace slot is missing: workspace/draft-$slot_number.md" >&2
    exit 1
  fi
done

echo "PASS: five default workspace draft slots are available"

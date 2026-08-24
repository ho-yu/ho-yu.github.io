#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"

for slot_number in 01 02 03 04 05 06 07 08 09 10; do
  slot_path="$repo_root/workspace/notes/note-$slot_number.md"
  if [[ ! -f "$slot_path" ]]; then
    echo "FAIL: required workspace slot is missing: workspace/notes/note-$slot_number.md" >&2
    exit 1
  fi
done

for slot_number in 01 02 03 04 05; do
  slot_path="$repo_root/workspace/projects/project-$slot_number.md"
  if [[ ! -f "$slot_path" ]]; then
    echo "FAIL: required workspace slot is missing: workspace/projects/project-$slot_number.md" >&2
    exit 1
  fi
done

echo "PASS: ten default note slots and five default project slots are available"

#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
override_base="$(mktemp)"
override_config="${override_base}.yml"
mv "$override_base" "$override_config"

cleanup() {
  rm "$override_config"
}
trap cleanup EXIT

printf '%s\n' 'exclude: []' >"$override_config"

cd "$repo_root"
set +e
check_output="$(bash tools/test-workspace-privacy.sh "_config.yml,$override_config" 2>&1)"
check_status=$?
set -e

if [[ $check_status -eq 0 ]]; then
  echo "FAIL: privacy test ignored the selected Jekyll config" >&2
  exit 1
fi

if [[ "$check_output" == *"WARNING: Error reading configuration"* ]]; then
  echo "FAIL: privacy test could not parse the selected Jekyll config" >&2
  exit 1
fi

if [[ "$check_output" != *"FAIL: workspace draft was included in the generated site:"* ]]; then
  echo "FAIL: privacy test failed for an unexpected reason" >&2
  printf '%s\n' "$check_output" >&2
  exit 1
fi

echo "PASS: privacy test honors the selected Jekyll config"

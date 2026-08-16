#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
workspace_dir="$repo_root/workspace"
config_files="${1:-_config.yml}"
probe_file=""

cleanup() {
  if [[ -n "$probe_file" && -f "$probe_file" ]]; then
    rm "$probe_file"
  fi
  rmdir "$workspace_dir" 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$workspace_dir"
probe_file="$(mktemp "$workspace_dir/exposure-check.XXXXXX.md")"
probe_name="$(basename "$probe_file")"

printf '%s\n' \
  '---' \
  'title: "Workspace exposure check"' \
  '---' \
  '' \
  'This file must never appear in the generated site.' >"$probe_file"

cd "$repo_root"
if bundle exec ruby -rjekyll -e '
  config_files = ARGV.fetch(1).split(",")
  site = Jekyll::Site.new(Jekyll.configuration("config" => config_files))
  site.read
  probe = ARGV.fetch(0)
  exposed = site.pages.any? { |page| page.path.end_with?(probe) } ||
    site.static_files.any? { |file| file.relative_path.end_with?(probe) }
  exit(exposed ? 0 : 1)
' "$probe_name" "$config_files"; then
  echo "FAIL: workspace draft was included in the generated site: $probe_name" >&2
  exit 1
fi

echo "PASS: workspace drafts are excluded from the generated site"

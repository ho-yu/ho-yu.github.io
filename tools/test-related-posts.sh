#!/usr/bin/env bash

set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
site_dir="${1:-_site}"
post_html="$site_dir/posts/vector-basics/index.html"

extract_related() {
  bundle exec ruby -rnokogiri -e '
    document = Nokogiri::HTML(File.read(ARGV.fetch(0)))
    related = document.at_css("#related-posts")
    print related.to_html if related
  ' "$1"
}

if [[ ! -f "$post_html" ]]; then
  echo "FAIL: related-post test page is missing: $post_html" >&2
  exit 1
fi

related_section="$(extract_related "$post_html")"
if [[ "$related_section" == *'/posts/start-developer-learning-log/'* ]]; then
  echo "FAIL: unrelated Meta post was recommended from the shared top-level Notes category" >&2
  exit 1
fi

fixture_root="$(mktemp -d)"
fixture_source="$fixture_root/source"
fixture_site="$fixture_root/site"

cleanup() {
  rm -rf "$fixture_root"
}
trap cleanup EXIT

mkdir -p "$fixture_source/_includes" "$fixture_source/_posts"
cp "$repo_root/_includes/related-posts.html" "$fixture_source/_includes/related-posts.html"
# related-posts.html renders each card's summary through our own excerpt include
cp "$repo_root/_includes/post-excerpt.html" "$fixture_source/_includes/post-excerpt.html"

printf '%s\n' \
  'theme: jekyll-theme-chirpy' \
  'lang: en' \
  'timezone: Asia/Seoul' \
  'url: https://example.test' \
  'permalink: /posts/:title/' \
  'defaults:' \
  '  - scope:' \
  '      path: ""' \
  '      type: posts' \
  '    values:' \
  '      layout: post' >"$fixture_source/_config.yml"

write_post() {
  filename="$1"
  title="$2"
  category="$3"
  tags="$4"

  printf '%s\n' \
    '---' \
    "title: \"$title\"" \
    "categories: [Notes, $category]" \
    "tags: [$tags]" \
    '---' \
    '' \
    "$title body." >"$fixture_source/_posts/$filename"
}

write_post '2020-01-01-ranking-target.md' 'Ranking Target' 'Fixture' 'alpha, beta'
write_post '2020-01-09-newer-strong.md' 'Newer Strong' 'Other' 'alpha, beta'
write_post '2020-01-08-older-strong.md' 'Older Strong' 'Other' 'alpha, beta'
write_post '2020-01-07-same-field.md' 'Same Field' 'Fixture' 'alpha'
write_post '2020-01-10-other-field.md' 'Other Field' 'Other' 'alpha'

write_post '2020-02-01-fallback-target.md' 'Fallback Target' 'Fallback' 'unique'
write_post '2020-02-02-fallback-match.md' 'Fallback Match' 'Fallback' 'other'
write_post '2020-02-03-top-level-only.md' 'Top Level Only' 'Unrelated' 'none'

write_post '2020-03-01-empty-target.md' 'Empty Target' 'Empty' 'isolated'

bundle exec jekyll build \
  --source "$fixture_source" \
  --destination "$fixture_site" \
  --config "$fixture_source/_config.yml" >/dev/null

ranking_section="$(extract_related "$fixture_site/posts/ranking-target/index.html")"

for expected_title in 'Newer Strong' 'Older Strong' 'Same Field'; do
  if [[ "$ranking_section" != *"$expected_title"* ]]; then
    echo "FAIL: expected related post is missing: $expected_title" >&2
    exit 1
  fi
done

if [[ "$ranking_section" == *'Other Field'* ]]; then
  echo "FAIL: same-field tie breaker did not beat the other-field candidate" >&2
  exit 1
fi

card_count="$(grep -o '<article class="col">' <<<"$ranking_section" | wc -l | tr -d ' ')"
if [[ "$card_count" -ne 3 ]]; then
  echo "FAIL: expected 3 related cards, found $card_count" >&2
  exit 1
fi

ranking_titles="$(bundle exec ruby -rnokogiri -e '
  document = Nokogiri::HTML(File.read(ARGV.fetch(0)))
  print document.css("#related-posts h4").map { |heading| heading.text.strip }.join("|")
' "$fixture_site/posts/ranking-target/index.html")"
if [[ "$ranking_titles" != 'Newer Strong|Older Strong|Same Field' ]]; then
  echo "FAIL: related post ranking is not deterministic: $ranking_titles" >&2
  exit 1
fi

if [[ "$ranking_section" != *'공통 주제 · alpha, beta'* ]]; then
  echo "FAIL: shared-tag relationship basis is missing" >&2
  exit 1
fi

fallback_section="$(extract_related "$fixture_site/posts/fallback-target/index.html")"
if [[ "$fallback_section" != *'Fallback Match'* || "$fallback_section" != *'같은 분야 · Fallback'* ]]; then
  echo "FAIL: second-level category fallback or its relationship basis is missing" >&2
  exit 1
fi

if [[ "$fallback_section" == *'Top Level Only'* ]]; then
  echo "FAIL: top-level category alone produced a fallback recommendation" >&2
  exit 1
fi

empty_section="$(extract_related "$fixture_site/posts/empty-target/index.html")"
if [[ -n "$empty_section" ]]; then
  echo "FAIL: empty related result rendered an unnecessary section" >&2
  exit 1
fi

echo "PASS: related posts ranking, fallback, limits, labels, and empty state are correct"

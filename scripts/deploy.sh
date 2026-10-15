#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
GH="${GH_BIN:-../.tools/gh}"
if ! command -v "$GH" >/dev/null 2>&1; then GH=gh; fi
account="$($GH api user --jq .login)"
if [[ "$account" != wangxidong06 ]]; then
  echo "Expected GitHub account wangxidong06; found $account. Aborting." >&2
  exit 1
fi
python scripts/build.py
python scripts/check.py
repo=wangxidong06/wangxidong06.github.io
# Verify existence explicitly; do not confuse an API outage with a missing repo.
status="$($GH api "repos/$repo" --include 2>/dev/null || true)"
if [[ "$status" == *'HTTP/2.0 404'* || "$status" == *'HTTP/1.1 404'* ]]; then
  "$GH" repo create "$repo" --public --description 'Xidong Wang — research, publications, and blog' --homepage https://wangxidong06.github.io
elif [[ "$status" == *'HTTP/2.0 200'* || "$status" == *'HTTP/1.1 200'* ]]; then
  if [[ ! -d .git ]] || ! git remote get-url origin >/dev/null 2>&1; then
    echo 'Repository already exists. Inspect it before connecting this checkout.' >&2
    exit 1
  fi
else
  echo 'Could not verify repository state. Check GitHub authentication or API availability.' >&2
  exit 1
fi
if [[ ! -d .git ]]; then git init -b main; fi
git config user.name 'Xidong Wang'
git config user.email 'wangxidong06@users.noreply.github.com'
"$GH" auth setup-git
git add index.html assets blog publications cv content scripts .github .gitignore .nojekyll README.md requirements.txt publications.json robots.txt sitemap.xml
if ! git diff --cached --quiet; then git commit -m 'Build academic homepage with publications and Markdown blog'; fi
if ! git remote get-url origin >/dev/null 2>&1; then git remote add origin "https://github.com/$repo.git"; fi
origin="$(git remote get-url origin)"
if [[ "$origin" != "https://github.com/$repo.git" ]]; then echo 'Unexpected origin; refusing to push.' >&2; exit 1; fi
# GitHub requires a nonempty repository before Pages can be enabled.
git push -u origin main
if "$GH" api "repos/$repo/pages" --silent 2>/dev/null; then
  "$GH" api --method PUT "repos/$repo/pages" -f build_type=workflow --silent
else
  "$GH" api --method POST "repos/$repo/pages" -f build_type=workflow --silent
fi
# Dispatch after enabling Pages; this also supersedes any initial setup run.
"$GH" workflow run pages.yml --repo "$repo" --ref main
echo 'Pushed. Track deployment with: gh run list --repo wangxidong06/wangxidong06.github.io --limit 1'

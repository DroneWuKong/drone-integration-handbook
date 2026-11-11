#!/usr/bin/env bash
set -euo pipefail

# Keep the image in sync with the Playwright version in package-lock.json.
image="mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$root/.local/browser-check"

# The software-only browser fixture uses loopback, not production services.
docker run --rm --init --network none \
  --user "$(id -u):$(id -g)" --env HOME=/tmp \
  --mount "type=bind,source=$root,target=/work,readonly" \
  --mount "type=bind,source=$root/.local/browser-check,target=/work/.local/browser-check" \
  --workdir /work "$image" npm run test:browser

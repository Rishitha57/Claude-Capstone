#!/bin/bash
set -e
echo "🔍 Scanning for accidental secret leaks..."
# Search for common API key patterns or hardcoded secrets
if git diff --cached | grep -E "(sk-[a-zA-Z0-9]{20,}|access_token|password\s*=\s*['\"][^'\"]+['\"] )"; then
  echo "❌ ERROR: Potential secret detected in staged changes!"
  exit 1
fi
echo "✅ Secret check passed."

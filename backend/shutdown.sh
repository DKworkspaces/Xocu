#!/bin/bash
echo "=== SAVE & EXIT TRIGGERED ==="

# 1. Configure the git bot identity
git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@://github.com"

# 2. Stage and commit the database file
git add form_data.db || true
git commit -m "chore: safe-exit administrative database sync [skip ci]" || echo "No changes recorded."
git push

echo "=== DATABASE SAVED. TERMINATING RUNNER RUN ==="
# 3. Kill the parent shell process to stop the GitHub Action instantly
pkill -9 -f "sleep 14400"
pkill -9 -f "uvicorn"

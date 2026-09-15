#!/bin/bash
echo "=== SAVE & EXIT TRIGGERED ==="

# 1. Configure the git bot identity
git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@://github.com"

# 2. Stage and commit the database file
git add form_data.db || true
git commit -m "chore: safe-exit administrative database sync [skip ci]" || echo "No changes recorded."
git push

echo "=== DATABASE SAVED. FORCING IMMEDIATE ACTION TERMINATION ==="

# 3. Kill every background process tied to this runner session cleanly
pkill -f "uvicorn"
pkill -f "lt" # Kills the localtunnel process
pkill -f "sleep"

# 4. The Ultimate Killswitch: Forces the entire GitHub Actions container job runner to end instantly
sudo kill -9 $(pgrep -f "runner/runners") || kill -9 $PPID

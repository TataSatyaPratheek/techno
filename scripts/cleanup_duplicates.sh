#!/usr/bin/env bash
# Safe cleanup script for migrating flat layout -> src/techno layout
# - Makes a timestamped backup of root-level duplicate folders
# - Moves presets/ into src/techno/presets if needed
# - Removes duplicate root-level folders
# - Cleans build artifacts and __pycache__
# - Prints final structure

set -euo pipefail
IFS=$'\n\t'

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="backup-flat-duplicates-$TS"
mkdir -p "$BACKUP_DIR"

echo "Repository root: $REPO_ROOT"
echo "Creating backup dir: $BACKUP_DIR"

# List of root-level duplicate folders to remove if present
DUP_DIRS=(cli core composition generators mixers processing techno)
DUP_FILES=(__init__.py)

# 1) Verify src/techno exists
if [ ! -d "src/techno" ]; then
  echo "ERROR: src/techno not found. Aborting to avoid accidental deletion."
  exit 1
fi

# 2) Move presets/ into src/techno/ if needed
if [ -d "presets" ] && [ ! -d "src/techno/presets" ]; then
  echo "Moving presets/ -> src/techno/presets/"
  mkdir -p src/techno
  mv presets src/techno/
  echo "Moved presets to src/techno/presets"
else
  echo "No presets/ move needed"
fi

# 3) Backup and remove duplicate root-level dirs/files
for d in "${DUP_DIRS[@]}"; do
  if [ -e "$d" ]; then
    echo "Backing up $d -> $BACKUP_DIR/"
    mv "$d" "$BACKUP_DIR/"
  else
    echo "Skipping $d (not present)"
  fi
done

for f in "${DUP_FILES[@]}"; do
  if [ -e "$f" ]; then
    echo "Backing up $f -> $BACKUP_DIR/"
    mv "$f" "$BACKUP_DIR/"
  else
    echo "Skipping $f (not present)"
  fi
done

# 4) Clean build artifacts
echo "Cleaning build artifacts: dist/ build/ *.egg-info htmlcov/"
rm -rf dist/ build/ *.egg-info htmlcov/ || true

# 5) Remove __pycache__ and *.pyc files
echo "Removing __pycache__ directories and .pyc files"
find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
find . -type f -name "*.pyc" -delete || true

# 6) Show final structure under src/techno and top-level files
echo "\nFinal src/techno structure (depth=3):"
if command -v tree >/dev/null 2>&1; then
  tree -L 3 src/techno || ls -R src/techno | sed -n '1,200p'
else
  find src/techno -maxdepth 3 -print | sed 's|^|  |'
fi

# 7) Summary of backup
echo "\nBackup of moved/removed items saved under: $BACKUP_DIR"
ls -la "$BACKUP_DIR" || true

cat <<EOF

Cleanup complete.
Next steps:
  1) Reinstall dev env: uv sync --dev
  2) Run tests: uv run pytest
  3) Commit changes: git add -A && git commit -m "Clean: migrate to src/techno layout" && git push
EOF

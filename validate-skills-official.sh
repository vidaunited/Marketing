#!/bin/bash
set -euo pipefail

# Validation script using official skills-ref library
# https://github.com/agentskills/agentskills/tree/main/skills-ref

# Resolve this repo's directory BEFORE any `cd`. The script used to run
# `cd "$(dirname "$0")"` after cd-ing into /tmp for the install step; with a
# relative $0 (e.g. `bash validate-skills-official.sh`) that resolved against
# /tmp/agentskills/skills-ref, so the first run validated nothing
# ("Path 'skills/*/' does not exist") and only a second run — which skips the
# install step and its cd — worked.
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="skills"
SKILLS_ROOT="/tmp/agentskills"
SKILLS_REF_DIR="$SKILLS_ROOT/skills-ref"

echo "🔍 Validating Skills Using Official skills-ref Library"
echo "========================================================"
echo "Reference: https://github.com/agentskills/agentskills"
echo ""

# Check if skills-ref is already installed
if [ ! -d "$SKILLS_REF_DIR/.venv" ]; then
    echo "📦 Installing skills-ref library..."
    echo ""

    if [ ! -d "$SKILLS_REF_DIR" ]; then
        git clone https://github.com/agentskills/agentskills.git "$SKILLS_ROOT"
    fi

    cd "$SKILLS_REF_DIR"

    if command -v uv &> /dev/null; then
        echo "Using uv to install..."
        uv sync
    else
        echo "Using pip to install..."
        python3 -m venv .venv
        # shellcheck disable=SC1091
        source .venv/bin/activate
        pip install -e .
    fi
    echo ""
fi

# Activate the virtual environment
# shellcheck disable=SC1091
source "$SKILLS_REF_DIR/.venv/bin/activate"

# Return to the repo directory captured above (never $0-relative after a cd)
cd "$REPO_DIR"

# Track results
PASSED=0
FAILED=0
FAILED_SKILLS=()

echo "Running validation..."
echo ""

# Validate each skill
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    printf "  %-30s" "$skill_name"

    # `|| true`: a failed validation must not abort the loop under `set -e`.
    output=$(skills-ref validate "$skill_dir" 2>&1) || true
    if echo "$output" | grep -q "Valid skill"; then
        echo "✓"
        PASSED=$((PASSED + 1))
    else
        echo "✗"
        FAILED=$((FAILED + 1))
        FAILED_SKILLS+=("$skill_name")
        echo "$output" | sed 's/^/    /'
    fi
done

echo ""
echo "========================================================"
echo "Summary:"
echo "  ✓ Passed: $PASSED"
echo "  ✗ Failed: $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "✅ All skills are valid!"
    exit 0
else
    echo "❌ Failed skills:"
    for skill in "${FAILED_SKILLS[@]}"; do
        echo "  - $skill"
    done
    exit 1
fi

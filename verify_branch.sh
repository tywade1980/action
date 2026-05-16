#!/bin/bash

# Verification script for agents-systems-only branch
# This script verifies that the branch was created correctly

echo "=========================================="
echo "Verifying agents-systems-only branch"
echo "=========================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if the branch exists
if ! git rev-parse --verify agents-systems-only >/dev/null 2>&1; then
    echo "❌ Error: agents-systems-only branch does not exist"
    exit 1
fi

echo "✅ Branch exists locally"
echo ""

# Switch to the branch
git checkout agents-systems-only 2>/dev/null

# Verify structure
echo "Checking branch contents..."
echo ""

# Count files
FILE_COUNT=$(find . -type f ! -path "./.git/*" | wc -l)
echo "📁 Total files: $FILE_COUNT (expected: 54)"

# Check for main directories
echo ""
echo "Checking directories:"
[ -d "1_deep_research/deep_research" ] && echo "✅ 1_deep_research/deep_research" || echo "❌ 1_deep_research/deep_research MISSING"
[ -d "2_engineering_team/engineering_team" ] && echo "✅ 2_engineering_team/engineering_team" || echo "❌ 2_engineering_team/engineering_team MISSING"
[ -d "3_trading_floor" ] && echo "✅ 3_trading_floor" || echo "❌ 3_trading_floor MISSING"

# Check for documentation files
echo ""
echo "Checking documentation:"
[ -f "README.md" ] && echo "✅ README.md ($(wc -c < README.md) bytes)" || echo "❌ README.md MISSING"
[ -f "QUICKSTART.md" ] && echo "✅ QUICKSTART.md ($(wc -c < QUICKSTART.md) bytes)" || echo "❌ QUICKSTART.md MISSING"
[ -f "TESTING.md" ] && echo "✅ TESTING.md ($(wc -c < TESTING.md) bytes)" || echo "❌ TESTING.md MISSING"
[ -f "ARCHITECTURE.md" ] && echo "✅ ARCHITECTURE.md ($(wc -c < ARCHITECTURE.md) bytes)" || echo "❌ ARCHITECTURE.md MISSING"

# Check for essential files
echo ""
echo "Checking essential files:"
[ -f "pyproject.toml" ] && echo "✅ pyproject.toml" || echo "❌ pyproject.toml MISSING"
[ -f ".gitignore" ] && echo "✅ .gitignore" || echo "❌ .gitignore MISSING"
[ -f "LICENSE" ] && echo "✅ LICENSE" || echo "❌ LICENSE MISSING"

# Check Deep Research files
echo ""
echo "Checking Deep Research system:"
DR_COUNT=$(find 1_deep_research/deep_research -name "*.py" 2>/dev/null | wc -l)
echo "   Python files: $DR_COUNT (expected: 6)"
[ -f "1_deep_research/deep_research/deep_research.py" ] && echo "   ✅ deep_research.py" || echo "   ❌ deep_research.py MISSING"
[ -f "1_deep_research/deep_research/research_manager.py" ] && echo "   ✅ research_manager.py" || echo "   ❌ research_manager.py MISSING"

# Check Engineering Team files
echo ""
echo "Checking Engineering Team system:"
[ -f "2_engineering_team/engineering_team/src/engineering_team/crew.py" ] && echo "   ✅ crew.py" || echo "   ❌ crew.py MISSING"
[ -f "2_engineering_team/engineering_team/src/engineering_team/config/agents.yaml" ] && echo "   ✅ agents.yaml" || echo "   ❌ agents.yaml MISSING"
[ -f "2_engineering_team/engineering_team/src/engineering_team/config/tasks.yaml" ] && echo "   ✅ tasks.yaml" || echo "   ❌ tasks.yaml MISSING"

# Check Trading Floor files
echo ""
echo "Checking Trading Floor system:"
TF_COUNT=$(find 3_trading_floor -maxdepth 1 -name "*.py" 2>/dev/null | wc -l)
echo "   Python files: $TF_COUNT (expected: 15)"
[ -f "3_trading_floor/trading_floor.py" ] && echo "   ✅ trading_floor.py" || echo "   ❌ trading_floor.py MISSING"
[ -f "3_trading_floor/traders.py" ] && echo "   ✅ traders.py" || echo "   ❌ traders.py MISSING"
[ -f "3_trading_floor/app.py" ] && echo "   ✅ app.py" || echo "   ❌ app.py MISSING"

# Check what's NOT in the branch (should be excluded)
echo ""
echo "Verifying exclusions (these should NOT exist):"
[ ! -d "guides" ] && echo "✅ guides/ excluded" || echo "❌ guides/ should be excluded"
[ ! -d "assets" ] && echo "✅ assets/ excluded" || echo "❌ assets/ should be excluded"
[ ! -d "setup" ] && echo "✅ setup/ excluded" || echo "❌ setup/ should be excluded"
[ ! -d "outputs" ] && echo "✅ outputs/ excluded" || echo "❌ outputs/ should be excluded"

# Summary
echo ""
echo "=========================================="
echo "Summary:"
echo "=========================================="

DOC_SIZE=$(wc -c *.md 2>/dev/null | tail -1 | awk '{print $1}')
echo "📚 Documentation: $DOC_SIZE bytes (~52KB expected)"
echo "📦 Files: $FILE_COUNT (54 expected)"
echo "🏗️  Agent Systems: 3 (Deep Research, Engineering Team, Trading Floor)"

# Check if pushed to remote
echo ""
if git ls-remote --heads origin agents-systems-only 2>/dev/null | grep -q agents-systems-only; then
    echo "✅ Branch is pushed to GitHub"
    echo "   Access at: https://github.com/tywade1980/action/tree/agents-systems-only"
else
    echo "⚠️  Branch is NOT pushed to GitHub yet"
    echo "   Run: git push -u origin agents-systems-only"
fi

echo ""
echo "=========================================="
echo "Verification complete!"
echo "=========================================="

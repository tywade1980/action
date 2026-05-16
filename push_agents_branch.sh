#!/bin/bash

# Script to push the agents-systems-only branch to GitHub
# Run this script after the work is complete

echo "=========================================="
echo "Pushing agents-systems-only branch"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Check if the branch exists
if ! git rev-parse --verify agents-systems-only >/dev/null 2>&1; then
    echo "Error: agents-systems-only branch does not exist"
    exit 1
fi

echo "Branch found locally. Attempting to push..."
echo ""

# Try to push the branch
git push -u origin agents-systems-only

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Branch pushed to remote."
    echo ""
    echo "Access the branch at:"
    echo "https://github.com/tywade1980/action/tree/agents-systems-only"
    echo ""
    echo "Or clone it directly:"
    echo "git clone --single-branch --branch agents-systems-only https://github.com/tywade1980/action.git"
else
    echo ""
    echo "⚠️  Push failed. You may need to:"
    echo "   1. Set up authentication (GitHub token or SSH key)"
    echo "   2. Have write permissions to the repository"
    echo ""
    echo "Manual push command:"
    echo "git push -u origin agents-systems-only"
fi

echo ""
echo "=========================================="

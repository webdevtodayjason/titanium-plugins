#!/bin/bash
# Cleanup Manual Titanium Toolkit Installation
#
# This script removes manually installed titanium-toolkit files from ~/.claude/
# Run this AFTER backing up with backup-manual-install.sh
#
# Usage: ./cleanup-manual-install.sh

set -e

# Determine repository root from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"

echo "🧹 Cleaning up manual Titanium Toolkit installation..."
echo ""
echo "⚠️  WARNING: This will remove titanium and BMAD files from ~/.claude/"
echo ""
echo "Make sure you ran ./backup-manual-install.sh first!"
echo ""
read -p "Continue with cleanup? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

echo ""
echo "Removing manual installations..."

REMOVED=0

# Remove titanium commands
if ls ~/.claude/commands/titanium-* 1> /dev/null 2>&1; then
    echo "🗑️  Removing titanium commands..."
    COUNT=$(ls ~/.claude/commands/titanium-* 2>/dev/null | wc -l)
    rm ~/.claude/commands/titanium-*
    echo "   ✅ Removed $COUNT command(s)"
    REMOVED=$((REMOVED + COUNT))
fi

# Remove BMAD commands
if ls ~/.claude/commands/bmad-* 1> /dev/null 2>&1; then
    echo "🗑️  Removing BMAD commands..."
    COUNT=$(ls ~/.claude/commands/bmad-* 2>/dev/null | wc -l)
    rm ~/.claude/commands/bmad-*
    echo "   ✅ Removed $COUNT command(s)"
    REMOVED=$((REMOVED + COUNT))
fi

# Remove workflow utilities
if [ -d ~/.claude/hooks/utils/workflow ]; then
    echo "🗑️  Removing workflow utilities..."
    COUNT=$(ls ~/.claude/hooks/utils/workflow/*.py 2>/dev/null | wc -l)
    rm -rf ~/.claude/hooks/utils/workflow
    echo "   ✅ Removed $COUNT utility(ies)"
    REMOVED=$((REMOVED + COUNT))
fi

# Remove BMAD utilities
if [ -d ~/.claude/hooks/utils/bmad ]; then
    echo "🗑️  Removing BMAD utilities..."
    COUNT=$(ls ~/.claude/hooks/utils/bmad/*.py 2>/dev/null | wc -l)
    rm -rf ~/.claude/hooks/utils/bmad
    echo "   ✅ Removed $COUNT utility(ies)"
    REMOVED=$((REMOVED + COUNT))
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Cleanup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Removed $REMOVED file(s) from ~/.claude/"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code"
echo "  2. Add marketplace:"
echo "     /plugin marketplace add ${REPO_ROOT}"
echo "  3. Install plugin:"
echo "     /plugin install titanium-toolkit@titanium-plugins"
echo "  4. Restart Claude Code again"
echo "  5. Commands will now use {{PLUGIN_DIR}} correctly"
echo "  6. Test: /bmad:start or /titanium:plan"
echo ""
echo "If you need to restore the manual installation:"
echo "  Check your backup in ~/.claude-archive/"
echo ""

#!/bin/bash
# Backup Manual Titanium Toolkit Installation
#
# This script backs up manually installed titanium-toolkit files from ~/.claude/
# before doing a proper marketplace installation.
#
# Usage: ./backup-manual-install.sh

set -e

# Determine repository root from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"

echo "🔄 Backing up manual Titanium Toolkit installation..."
echo ""

# Create timestamped backup directory
BACKUP_DIR="$HOME/.claude-archive/titanium-manual-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Backup location: $BACKUP_DIR"
echo ""

# Track what we backup
BACKED_UP=0

# Backup titanium commands
if ls ~/.claude/commands/titanium-* 1> /dev/null 2>&1; then
    echo "📄 Backing up titanium commands..."
    mkdir -p "$BACKUP_DIR/commands"
    cp -a ~/.claude/commands/titanium-* "$BACKUP_DIR/commands/"
    TITANIUM_CMD_COUNT=$(ls ~/.claude/commands/titanium-* 2>/dev/null | wc -l)
    echo "   ✅ Backed up $TITANIUM_CMD_COUNT titanium command(s)"
    BACKED_UP=$((BACKED_UP + TITANIUM_CMD_COUNT))
fi

# Backup BMAD commands
if ls ~/.claude/commands/bmad-* 1> /dev/null 2>&1; then
    echo "📄 Backing up BMAD commands..."
    mkdir -p "$BACKUP_DIR/commands"
    cp -a ~/.claude/commands/bmad-* "$BACKUP_DIR/commands/"
    BMAD_CMD_COUNT=$(ls ~/.claude/commands/bmad-* 2>/dev/null | wc -l)
    echo "   ✅ Backed up $BMAD_CMD_COUNT BMAD command(s)"
    BACKED_UP=$((BACKED_UP + BMAD_CMD_COUNT))
fi

# Backup workflow utilities
if [ -d ~/.claude/hooks/utils/workflow ]; then
    echo "🔧 Backing up workflow utilities..."
    mkdir -p "$BACKUP_DIR/utils"
    cp -r ~/.claude/hooks/utils/workflow "$BACKUP_DIR/utils/"
    WORKFLOW_COUNT=$(ls ~/.claude/hooks/utils/workflow/*.py 2>/dev/null | wc -l)
    echo "   ✅ Backed up $WORKFLOW_COUNT workflow utility(ies)"
    BACKED_UP=$((BACKED_UP + WORKFLOW_COUNT))
fi

# Backup BMAD utilities
if [ -d ~/.claude/hooks/utils/bmad ]; then
    echo "🔧 Backing up BMAD utilities..."
    mkdir -p "$BACKUP_DIR/utils"
    cp -r ~/.claude/hooks/utils/bmad "$BACKUP_DIR/utils/"
    BMAD_UTIL_COUNT=$(ls ~/.claude/hooks/utils/bmad/*.py 2>/dev/null | wc -l)
    echo "   ✅ Backed up $BMAD_UTIL_COUNT BMAD utility(ies)"
    BACKED_UP=$((BACKED_UP + BMAD_UTIL_COUNT))
fi

# Create backup manifest
cat > "$BACKUP_DIR/BACKUP_INFO.md" << EOF
# Titanium Toolkit Manual Installation Backup

**Backup Date**: $(date)
**Backup Location**: $BACKUP_DIR
**Files Backed Up**: $BACKED_UP

## What Was Backed Up

- Titanium commands (titanium-*)
- BMAD commands (bmad-*)
- Workflow utilities (workflow/)
- BMAD utilities (bmad/)

## Why This Backup

These files were manually copied to ~/.claude/ for testing.
Now installing properly via plugin marketplace.

## Restore Instructions

If you need to restore this manual installation:

\`\`\`bash
# Restore commands
cp $BACKUP_DIR/commands/* ~/.claude/commands/

# Restore utilities
cp -r $BACKUP_DIR/utils/* ~/.claude/hooks/utils/

# Restart Claude Code
\`\`\`

## Next Steps

After this backup:
1. Remove manual installations (run cleanup script)
2. Restart Claude Code
3. Add marketplace: /plugin marketplace add $REPO_ROOT
4. Install plugin: /plugin install titanium-toolkit@titanium-plugins
5. Restart Claude Code again
6. Test: /bmad:start or /titanium:plan

EOF

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Backup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Backed up $BACKED_UP file(s) to:"
echo "  $BACKUP_DIR"
echo ""
echo "Backup manifest:"
echo "  $BACKUP_DIR/BACKUP_INFO.md"
echo ""
echo "Next steps:"
echo "  1. Run: ./cleanup-manual-install.sh"
echo "  2. Restart Claude Code"
echo "  3. Install from marketplace:"
echo "     /plugin marketplace add ${REPO_ROOT}"
echo "     /plugin install titanium-toolkit@titanium-plugins"
echo "  4. Restart Claude Code"
echo "  5. Test: /bmad:start"
echo ""

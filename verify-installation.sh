#!/bin/bash
# Titanium Toolkit Installation Verification Script
#
# This script verifies that all requirements are met for Titanium Toolkit
#
# Usage: ./verify-installation.sh

set -e

echo "🔍 Titanium Toolkit Installation Verification"
echo "=============================================="
echo ""

ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Claude Code
echo "📦 Checking Software Requirements..."
echo ""

# Check UV
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version 2>&1 | head -1)
    echo -e "${GREEN}✅ UV installed:${NC} $UV_VERSION"
else
    echo -e "${RED}❌ UV not found${NC}"
    echo "   Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    ERRORS=$((ERRORS + 1))
fi

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC} (requires 3.11+)"
    else
        echo -e "${RED}❌ Python $PYTHON_VERSION${NC} (requires 3.11+)"
        echo "   Install Python 3.11+ from python.org"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ Python not found${NC}"
    echo "   Install Python 3.11+ from python.org"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "🔑 Checking API Keys..."
echo ""

# Check Anthropic API key (required for planning and BMAD)
if [ -f ~/.env ] && grep -q "ANTHROPIC_API_KEY" ~/.env; then
    ANTHROPIC_KEY=$(grep "ANTHROPIC_API_KEY" ~/.env | cut -d= -f2)
    if [ -n "$ANTHROPIC_KEY" ] && [ "$ANTHROPIC_KEY" != "sk-ant-your-key-here" ]; then
        echo -e "${GREEN}✅ ANTHROPIC_API_KEY found${NC} in ~/.env"
    else
        echo -e "${RED}❌ ANTHROPIC_API_KEY not set${NC} in ~/.env"
        echo "   Required for /titanium:plan and /bmad:start"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ ~/.env not found or no ANTHROPIC_API_KEY${NC}"
    echo "   Required for /titanium:plan and /bmad:start"
    echo "   Create: echo 'ANTHROPIC_API_KEY=sk-ant-your-key' >> ~/.env"
    ERRORS=$((ERRORS + 1))
fi

# Check OpenAI API key (required for voice summaries)
if [ -f ~/.env ] && grep -q "OPENAI_API_KEY" ~/.env; then
    OPENAI_KEY=$(grep "OPENAI_API_KEY" ~/.env | cut -d= -f2)
    if [ -n "$OPENAI_KEY" ] && [ "$OPENAI_KEY" != "your_openai_key_here" ]; then
        echo -e "${GREEN}✅ OPENAI_API_KEY found${NC} in ~/.env (for voice summaries)"
    else
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set${NC} (voice will use simple text)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY not found${NC} (voice will use simple text)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check ElevenLabs API key (optional)
if [ -f ~/.env ] && grep -q "ELEVENLABS_API_KEY" ~/.env; then
    ELEVENLABS_KEY=$(grep "ELEVENLABS_API_KEY" ~/.env | cut -d= -f2)
    if [ -n "$ELEVENLABS_KEY" ] && [ "$ELEVENLABS_KEY" != "your_elevenlabs_key_here" ]; then
        echo -e "${GREEN}✅ ELEVENLABS_API_KEY found${NC} in ~/.env (voice enabled)"
    else
        echo -e "${YELLOW}⚠️  ELEVENLABS_API_KEY not set${NC} (voice will use macOS say)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️  ELEVENLABS_API_KEY not found${NC} (voice will use macOS say)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check vibe-check config (optional)
if [ -f ~/.vibe-check/.env ]; then
    if grep -qE "(GEMINI_API_KEY|OPENAI_API_KEY|OPENROUTER_API_KEY)" ~/.vibe-check/.env; then
        echo -e "${GREEN}✅ vibe-check configured${NC} (quality gates enabled)"
    else
        echo -e "${YELLOW}⚠️  vibe-check config exists but no API key${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️  vibe-check not configured${NC} (quality gates disabled)"
    echo "   Optional but recommended for AI quality validation"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "🧪 Testing Utilities..."
echo ""

# Test workflow_state.py
if [ -f ~/.claude/hooks/utils/workflow/workflow_state.py ]; then
    if uv run ~/.claude/hooks/utils/workflow/workflow_state.py 2>&1 | grep -q "Usage:"; then
        echo -e "${GREEN}✅ workflow_state.py works${NC}"
    else
        echo -e "${RED}❌ workflow_state.py failed${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ workflow_state.py not found${NC}"
    echo "   Expected at: ~/.claude/hooks/utils/workflow/workflow_state.py"
    ERRORS=$((ERRORS + 1))
fi

# Test plan_parser.py
if [ -f ~/.claude/hooks/utils/workflow/plan_parser.py ]; then
    if uv run ~/.claude/hooks/utils/workflow/plan_parser.py 2>&1 | grep -qE "(Usage:|OPENAI_API_KEY)"; then
        echo -e "${GREEN}✅ plan_parser.py works${NC}"
    else
        echo -e "${RED}❌ plan_parser.py failed${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ plan_parser.py not found${NC}"
    echo "   Expected at: ~/.claude/hooks/utils/workflow/plan_parser.py"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "📋 Checking Commands..."
echo ""

# Check if commands exist
COMMANDS=(
    "catchup.md"
    "titanium-plan.md"
    "titanium-work.md"
    "titanium-review.md"
    "titanium-status.md"
)

for cmd in "${COMMANDS[@]}"; do
    if [ -f ~/.claude/commands/$cmd ]; then
        echo -e "${GREEN}✅ /$cmd${NC}"
    else
        echo -e "${RED}❌ /$cmd not found${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "🎤 Checking Voice System..."
echo ""

# Check if say works (macOS fallback)
if command -v say &> /dev/null; then
    echo -e "${GREEN}✅ macOS say available${NC} (voice fallback works)"
else
    echo -e "${YELLOW}⚠️  macOS say not available${NC} (not on macOS?)"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "🤖 Checking Optional: CodeRabbit CLI..."
echo ""

# Check CodeRabbit (optional but recommended)
if command -v coderabbit &> /dev/null; then
    CR_VERSION=$(coderabbit --version 2>&1 | head -1 || echo "installed")
    echo -e "${GREEN}✅ CodeRabbit CLI installed${NC} ($CR_VERSION)"

    # Check auth status
    if coderabbit auth status 2>&1 | grep -qi "authenticated\|logged in"; then
        echo -e "${GREEN}   ✅ Authenticated${NC} (enhanced reviews enabled)"
    else
        echo -e "${YELLOW}   ⚠️  Not authenticated${NC} (run: coderabbit auth login for enhanced reviews)"
    fi
else
    echo -e "${YELLOW}⚠️  CodeRabbit CLI not found${NC} (optional but recommended)"
    echo "   Install: curl -fsSL https://cli.coderabbit.ai/install.sh | sh"
    echo "   Provides: Deep static analysis, race condition detection, memory leak detection"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "=============================================="
echo ""

# Summary
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed!${NC}"
    echo ""
    echo "Titanium Toolkit is ready to use!"
    echo ""
    echo "Try: /titanium:plan \"Add a contact form\""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS warnings (optional features)${NC}"
    echo -e "${GREEN}✅ Core functionality ready!${NC}"
    echo ""
    echo "Titanium Toolkit will work, but some features are optional."
    echo "See warnings above for enhancement options."
    echo ""
    echo "Try: /titanium:plan \"Add a contact form\""
    exit 0
else
    echo -e "${RED}❌ $ERRORS errors found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS warnings${NC}"
    fi
    echo ""
    echo "Please fix the errors above before using Titanium Toolkit."
    echo ""
    echo "See: https://github.com/webdevtodayjason/titanium-plugins#requirements"
    exit 1
fi

# Titanium Toolkit - Dependencies Guide

**Version**: 2.0.0
**Last Updated**: October 2025

---

## The Good News: UV Handles Everything!

All Titanium Toolkit Python scripts use **UV's inline dependency format**. This means:

✅ **No `pip install` needed**
✅ **No `requirements.txt` to manage**
✅ **No virtual environments to activate**
✅ **Dependencies install automatically when script runs**

---

## How UV Works

Every Python script in Titanium Toolkit has this header:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///
```

**When you run the script**, UV:
1. Checks if dependencies are installed
2. Installs them if needed (in isolated cache)
3. Runs the script
4. No global pollution of your Python environment

**First run**: UV installs dependencies (~3 seconds)
**Subsequent runs**: UV uses cache (instant)

---

## All Dependencies Used

### Complete Dependency List

Here are ALL dependencies used across Titanium Toolkit:

| Package | Used By | Purpose |
|---------|---------|---------|
| **python-dotenv** | All scripts (11 files) | Load API keys from .env files |
| **openai** | 6 scripts | GPT-4 planning, GPT-5 summaries |
| **elevenlabs** | 1 script | High-quality voice synthesis |
| **anthropic** | 1 script | Claude API (future use) |
| **pyttsx3** | 1 script | Local TTS fallback |

### By Script

**Workflow Utilities**:
- `workflow_state.py`: python-dotenv
- `plan_parser.py`: python-dotenv, openai

**Voice Hooks**:
- `post_tool_use_elevenlabs.py`: python-dotenv, openai
- `stop.py`: python-dotenv, openai
- `notification.py`: python-dotenv, openai
- `subagent_stop.py`: python-dotenv

**TTS Utilities**:
- `elevenlabs_tts.py`: elevenlabs, python-dotenv
- `openai_tts.py`: openai, python-dotenv
- `elevenlabs_mcp.py`: python-dotenv
- `local_tts.py`: pyttsx3

**LLM Utilities**:
- `oai.py`: openai, python-dotenv
- `anth.py`: anthropic, python-dotenv

---

## User Installation Requirements

### What Users Need to Install

**1. UV (Required)**
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

**2. Python 3.11+ (Required)**
```bash
# Check version
python3 --version

# If < 3.11, install from python.org
```

**That's it!** UV handles all Python package dependencies automatically.

### What Users DON'T Need

❌ Don't need to run `pip install`
❌ Don't need virtual environments
❌ Don't need to manage requirements.txt
❌ Don't need to install openai, elevenlabs, etc. manually

UV does it all!

---

## How UV Installs Dependencies

### First Time Running a Script

```bash
$ /titanium:plan "Add authentication"

# Claude runs: uv run plan_parser.py
# UV output:
Downloading openai
Downloading pydantic
Downloading python-dotenv
Installed 17 packages in 3s

# Then script runs normally
```

### Subsequent Runs

```bash
$ /titanium:work

# Claude runs scripts
# UV output:
Installed 1 package in 4ms  # Already cached, instant

# Scripts run immediately
```

### Where UV Stores Dependencies

UV caches dependencies in:
- **macOS/Linux**: `~/.cache/uv/`
- **Windows**: `%LOCALAPPDATA%\uv\cache\`

This is per-user, isolated from system Python.

---

## Verification Script

To verify UV and dependencies work correctly:

```bash
# Create verification script
cat > /tmp/verify-titanium-deps.sh << 'EOF'
#!/bin/bash

echo "🔍 Verifying Titanium Toolkit Dependencies..."
echo ""

# Check UV installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV not found"
    echo "Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo "✅ UV installed: $(uv --version)"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.11"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION found, need 3.11+"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION (requires 3.11+)"

# Test workflow_state.py
echo ""
echo "Testing workflow utilities..."
if uv run ~/.claude/hooks/utils/workflow/workflow_state.py 2>&1 | grep -q "Usage:"; then
    echo "✅ workflow_state.py works"
else
    echo "❌ workflow_state.py failed"
    exit 1
fi

# Test plan_parser.py (will fail without OpenAI key, but should load dependencies)
if uv run ~/.claude/hooks/utils/workflow/plan_parser.py 2>&1 | grep -qE "(Usage:|OPENAI_API_KEY)"; then
    echo "✅ plan_parser.py loads (OpenAI key needed for actual use)"
else
    echo "❌ plan_parser.py failed to load"
    exit 1
fi

echo ""
echo "✅ All dependency checks passed!"
echo ""
echo "Note: Some scripts need API keys to fully function:"
echo "  - OPENAI_API_KEY (required for planning)"
echo "  - ELEVENLABS_API_KEY (optional for voice)"
echo ""
echo "Add to ~/.env and restart Claude Code"
EOF

chmod +x /tmp/verify-titanium-deps.sh
/tmp/verify-titanium-deps.sh
```

---

## For Plugin Developers

### Adding New Scripts

When creating new Python utilities:

**Always use UV script format**:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "package-name",
#     "another-package>=1.0.0",
# ]
# ///

import package_name

def main():
    # Your code here
    pass

if __name__ == "__main__":
    main()
```

**Benefits**:
- Users don't need to install dependencies
- Isolated from system Python
- Reproducible across machines
- Self-documenting

### Testing Dependencies

```bash
# Test your script
uv run your_script.py

# First run: UV installs dependencies
# Subsequent runs: Uses cache (fast)
```

---

## For Advanced Users

### Listing All Dependencies

To see all packages UV will install:

```bash
# Scan all scripts
find plugins/titanium-toolkit -name "*.py" -exec grep -A 5 "# dependencies" {} \;
```

### Pre-warming UV Cache

To install all dependencies ahead of time:

```bash
# Run each utility once
cd plugins/titanium-toolkit/hooks/utils/workflow
uv run workflow_state.py
uv run plan_parser.py requirements.md "$(pwd)" 2>&1 || true

cd ../tts
uv run elevenlabs_tts.py "Test" 2>&1 || true
uv run openai_tts.py "Test" 2>&1 || true

cd ../llm
uv run oai.py "Test" 2>&1 || true
uv run anth.py "Test" 2>&1 || true
```

This downloads all dependencies to cache. Scripts will be instant afterwards.

---

## Troubleshooting Dependencies

### "uv: command not found"

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"

# Verify
uv --version
```

### "Package installation failed"

```bash
# Clear UV cache
rm -rf ~/.cache/uv

# Try again
uv run your_script.py
```

### "Python version too old"

```bash
# Check version
python3 --version

# If < 3.11, install from:
# macOS: brew install python@3.11
# Linux: apt install python3.11
# Windows: python.org
```

---

## Reference: requirements.txt Equivalent

For documentation purposes, here's what a traditional requirements.txt would look like (NOT NEEDED with UV):

```txt
# TTS Dependencies
elevenlabs>=1.0.0
pyttsx3>=2.90

# LLM Dependencies
openai>=1.0.0
anthropic>=0.25.0

# Utilities
python-dotenv>=1.0.0
```

**Again: Users DON'T need to install these!** UV handles it automatically.

---

## Summary

### For Users

✅ **Just install UV** (one command)
✅ **Python 3.11+** (check version)
✅ **Add API keys** to ~/.env
✅ **That's it!**

Dependencies install automatically when you use Titanium Toolkit commands.

### For Developers

✅ **Always use UV script format** with inline dependencies
✅ **Test scripts with `uv run`**
✅ **No global package installation needed**
✅ **Dependencies are self-contained and versioned**

---

## Installation Checklist

When installing Titanium Toolkit, users need:

- [ ] Claude Code 2.0.14+
- [ ] Python 3.11+
- [ ] UV installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] OpenAI API key in ~/.env
- [ ] (Optional) ElevenLabs API key in ~/.env
- [ ] (Optional) vibe-check API key in ~/.vibe-check/.env
- [ ] (Optional) Pieces OS + CLI

**After installation**: First script run will install Python dependencies automatically via UV. Subsequent runs are instant.

---

**The beauty of UV**: Users install the plugin and it just works. No dependency management needed!

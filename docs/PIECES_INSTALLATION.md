# Pieces Installation Guide

Complete guide for installing and configuring Pieces OS and Pieces CLI for use with Titanium Toolkit.

## Overview

Pieces provides long-term memory (LTM) for your development workflow, capturing everything you do across applications. The Titanium Toolkit's `/catchup` command queries this memory to help you resume work instantly.

## Prerequisites

- **macOS** 11.0+, **Windows** 10+, or **Linux** (Ubuntu 20.04+)
- **Python** 3.8+
- **Disk Space**: ~500MB for Pieces OS

## Step 1: Install Pieces OS

Pieces OS is the core engine that captures and stores your workflow context.

### macOS

**Option 1: Direct Download**
1. Visit https://pieces.app
2. Click "Download for Mac"
3. Open the downloaded DMG file
4. Drag "Pieces OS" to Applications folder
5. Launch Pieces OS from Applications

**Option 2: Homebrew**
```bash
brew install --cask pieces-os
```

### Windows

1. Visit https://pieces.app
2. Click "Download for Windows"
3. Run the installer (.exe)
4. Follow installation wizard
5. Launch Pieces OS from Start Menu

### Linux

**Ubuntu/Debian:**
```bash
# Download the latest .deb package
wget https://builds.pieces.app/stages/production/pieces-os/linux/pieces-os_latest.deb

# Install
sudo dpkg -i pieces-os_latest.deb

# Fix dependencies if needed
sudo apt-get install -f
```

**Arch Linux:**
```bash
yay -S pieces-os
```

## Step 2: Configure Pieces OS

1. **Launch Pieces OS** (menu bar icon should appear)
2. **Sign in/Create Account** when prompted
3. **Enable Long-Term Memory (LTM-2.7)**:
   - Click Pieces OS icon in menu bar
   - Open Settings
   - Navigate to "Long-Term Memory"
   - Toggle "Enable LTM" to ON
   - Configure which applications to track (enable all for best results)

4. **Verify Pieces OS is Running**:
   ```bash
   # Check if Pieces OS process is running
   ps aux | grep "Pieces OS" | grep -v grep
   ```

You should see Pieces OS running in the process list.

## Step 3: Install Pieces CLI

The Pieces CLI provides the MCP server interface for Claude Code.

### Via pip (Recommended)

```bash
# Upgrade pip first
python3 -m pip install --upgrade pip

# Install Pieces CLI
pip3 install --upgrade pieces-cli
```

### Verify Installation

```bash
# Check pieces command is available
which pieces

# Should output something like:
# /usr/local/bin/pieces
# or
# /Users/yourname/Library/Python/3.x/bin/pieces

# Check version
pieces --version
```

## Step 4: Configure Pieces MCP for Claude Code

Now connect Pieces to Claude Code via MCP:

```bash
# Run the automatic setup (recommended)
pieces mcp setup claude_code --stdio
```

This command:
- Detects your Claude Code configuration location
- Adds Pieces MCP server entry to `~/.claude.json`
- Configures proper stdio transport

**Alternative: Manual Configuration**

If the automatic setup fails, manually add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "Pieces": {
      "command": "/path/to/pieces",
      "args": [
        "--ignore-onboarding",
        "mcp",
        "start"
      ]
    }
  }
}
```

Replace `/path/to/pieces` with the output from `which pieces`.

## Step 5: Verify Setup

### Test Pieces MCP Connection

```bash
# List all MCP servers
claude mcp list
```

You should see:
```
Pieces: /path/to/pieces --ignore-onboarding mcp start - ✓ Connected
```

### Test Pieces LTM Query

Start Claude Code and try:

```bash
/catchup
```

You should see Claude query your Pieces LTM and provide context about your recent work.

## Troubleshooting

### Pieces MCP shows "✘ failed"

**Solution 1: Verify Pieces OS is running**
```bash
ps aux | grep "Pieces OS"
```

If not running, launch Pieces OS from Applications.

**Solution 2: Check Pieces CLI path**
```bash
which pieces
```

Update `~/.claude.json` with the correct path if needed.

**Solution 3: Reinstall Pieces CLI**
```bash
pip3 uninstall pieces-cli
pip3 install --upgrade pieces-cli
```

### "/catchup command not found"

**Solution**: Ensure titanium-toolkit plugin is installed:
```bash
/plugin marketplace add webdevtodayjason/titanium-plugins
/plugin install titanium-toolkit
```

Restart Claude Code after installation.

### "No context found" when using /catchup

**Solution 1: Enable LTM in Pieces**
- Open Pieces OS settings
- Enable Long-Term Memory
- Configure application tracking

**Solution 2: Give Pieces time to capture context**
- LTM needs time to build context
- Work for 10-15 minutes with various applications
- Try `/catchup` again

**Solution 3: Check LTM data**
- Open Pieces Desktop app
- View "Workstream Activity"
- Verify events are being captured

### Pieces CLI not in PATH

**macOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/Library/Python/3.x/bin:$PATH"

# Reload shell
source ~/.zshrc  # or ~/.bashrc
```

**Windows:**
Add Python Scripts directory to System PATH via Environment Variables.

## Advanced Configuration

### Custom LTM Settings

Configure what Pieces captures:

1. Open Pieces OS Settings
2. Go to "Long-Term Memory"
3. Configure:
   - Applications to track
   - Data retention period
   - Privacy settings
   - Capture frequency

### Pieces API Access

For advanced integrations, get your Pieces API token:

```bash
pieces config
```

## Additional Resources

- **Pieces Documentation**: https://docs.pieces.app
- **Pieces MCP Guide**: https://docs.pieces.app/products/mcp/get-started
- **Claude Code MCP Docs**: https://docs.claude.com/en/docs/claude-code/mcp
- **Titanium Toolkit Issues**: https://github.com/webdevtodayjason/titanium-plugins/issues

## Need Help?

- **Pieces Support**: https://docs.pieces.app/support
- **Titanium Toolkit Issues**: https://github.com/webdevtodayjason/titanium-plugins/issues
- **Claude Developers Discord**: https://anthropic.com/discord

---

Once Pieces is properly installed and configured, the `/catchup` command in Titanium Toolkit will provide powerful context recovery for all your Claude Code sessions!

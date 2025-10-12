# Titanium Plugins - Claude Development Guide

This document provides guidance for Claude when working on the titanium-plugins marketplace repository.

## Repository Purpose

This is a Claude Code plugin marketplace created and maintained by Jason Brashear (Titanium Computing). It distributes the **titanium-toolkit** plugin, which provides voice-enhanced AI development workflows.

## Core Philosophy

**Voice-Enhanced Development**: Every interaction should provide audio feedback to keep developers informed without breaking their flow. The voice system uses ElevenLabs for quality and GPT-5 models for intelligent summarization.

## Repository Structure

```
titanium-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest - lists all plugins
├── .gitignore                     # Protects API keys and secrets
├── LICENSE                        # MIT License
├── README.md                      # Public documentation
├── CLAUDE.md                      # This file - Claude's development guide
└── plugins/
    └── titanium-toolkit/          # The flagship plugin
        ├── .claude-plugin/
        │   └── plugin.json        # Plugin manifest
        ├── agents/                # 16 builder agents
        ├── commands/              # Slash commands
        ├── hooks/                 # Voice system hooks
        │   ├── hooks.json         # Hook configuration
        │   ├── post_tool_use_elevenlabs.py
        │   ├── stop.py
        │   ├── notification.py
        │   ├── subagent_stop.py
        │   └── utils/
        │       ├── tts/           # Text-to-speech utilities
        │       └── llm/           # LLM helper scripts
        ├── LICENSE
        └── README.md
```

## Working with This Repository

### Adding a New Plugin

1. Create plugin directory:
   ```bash
   mkdir -p plugins/new-plugin-name/{.claude-plugin,agents,commands,hooks}
   ```

2. Create plugin manifest:
   ```json
   {
     "name": "new-plugin-name",
     "version": "1.0.0",
     "description": "Plugin description",
     "author": {
       "name": "Jason Brashear",
       "email": "jason@webdevtoday.com"
     },
     "license": "MIT"
   }
   ```

3. Update marketplace manifest (`.claude-plugin/marketplace.json`):
   ```json
   "plugins": [
     {
       "name": "new-plugin-name",
       "source": "./plugins/new-plugin-name",
       "description": "Brief description"
     }
   ]
   ```

4. Add README.md to the plugin directory

### Updating Existing Plugins

When modifying titanium-toolkit:

- **Agents**: Add/edit markdown files in `plugins/titanium-toolkit/agents/`
- **Commands**: Add/edit markdown files in `plugins/titanium-toolkit/commands/`
- **Hooks**: Modify Python scripts in `plugins/titanium-toolkit/hooks/`
- **Version**: Increment version in `plugin.json` following semver

### Voice Hook System

**CRITICAL**: The voice hooks are the unique feature of this marketplace.

**Components:**
1. **post_tool_use_elevenlabs.py** - Announces tool completions
   - Uses GPT-5 nano for summaries
   - Skips: TodoWrite, Grep, LS, Bash, Read, Glob, WebFetch, WebSearch
   - Voice: ElevenLabs Sarah (fallback to macOS say)

2. **stop.py** - Session end summaries
   - Uses GPT-5 mini for comprehensive summaries
   - Analyzes entire transcript
   - Voice: ElevenLabs Sarah

3. **notification.py** - User attention alerts
   - Uses GPT-5 nano for context-aware messages
   - Alert sound + voice
   - Voice: ElevenLabs Sarah

4. **subagent_stop.py** - Agent completion announcements

**When modifying voice hooks:**
- NEVER hardcode API keys
- Always use `os.getenv()` for secrets
- Test with both ElevenLabs and fallback
- Update skip lists in post_tool_use if needed
- Use GPT-5 models: `max_completion_tokens` (NOT `max_tokens`)
- GPT-5 models don't support custom temperature

### Testing Changes Locally

1. **Add local marketplace:**
   ```bash
   /plugin marketplace add /Users/sem/titanium-plugins
   ```

2. **Install plugin:**
   ```bash
   /plugin install titanium-toolkit@titanium-plugins
   ```

3. **Test components:**
   - Commands: `/catchup`
   - Agents: `@api-developer`, `@frontend-developer`
   - Voice: Edit a file and listen for announcement

4. **Uninstall and reinstall** after changes:
   ```bash
   /plugin uninstall titanium-toolkit@titanium-plugins
   /plugin install titanium-toolkit@titanium-plugins
   ```

### API Keys and Security

**NEVER commit:**
- API keys (OpenAI, ElevenLabs, etc.)
- SSH private keys
- .env files with secrets

**.gitignore protects:**
- `.env` files
- `*.key` files
- `*.pem` files
- `logs/` directories

**Documentation should instruct users to:**
- Add API keys to `~/.env`
- Set permissions: `chmod 600 ~/.env`

### Commit Conventions

Use clear, descriptive commit messages:

**Format:**
```
type: Brief description

- Detailed point 1
- Detailed point 2
```

**Types:**
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

**Examples:**
- `feat: Add meta-agent for creating custom agents`
- `docs: Update voice system architecture diagram`
- `fix: Correct ElevenLabs import path`

### Version Management

Follow semantic versioning (semver):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features (backwards compatible)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

Update version in:
- `plugins/titanium-toolkit/.claude-plugin/plugin.json`
- Git tag: `git tag v1.0.1`

### Integration with Other Tools

**BMAD-METHOD:**
- Users install BMAD separately for PRD creation
- Output: `~/bmad/output/*.md` files
- These feed into `/compounding-engineering:work` command

**compounding-engineering plugin:**
- Users install from Every's marketplace
- Provides `/work`, `/review`, `/plan` commands
- Uses titanium-toolkit's agents for implementation

**Pieces:**
- Required for `/catchup` command
- Users must install Pieces OS and CLI
- MCP configuration: `pieces mcp setup claude_code --stdio`

### GPT-5 Model Usage

**Current configuration:**
- **GPT-5 nano** ($0.05/1M tokens):
  - post_tool_use summaries (3-7 words)
  - notification messages (context-aware)

- **GPT-5 mini** ($0.25/1M tokens):
  - Session summaries (1-2 sentences)

**Important:**
- Use `max_completion_tokens` (NOT `max_tokens`)
- Don't set `temperature` (GPT-5 uses default only)
- Keep prompts focused and concise

### Voice Configuration

**ElevenLabs:**
- Voice ID: `EXAVITQu4vr4xnSDxMaL` (Sarah)
- Model: `eleven_turbo_v2_5`
- Format: `mp3_44100_128`

**Fallback:**
- macOS `say` command (always available)
- No API key required

### Resources

**Documentation:**
- Claude Code Plugins: https://docs.claude.com/en/docs/claude-code/plugins
- Plugin Reference: https://docs.claude.com/en/docs/claude-code/plugins-reference
- Every Marketplace: https://github.com/EveryInc/every-marketplace
- BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD

**Credits:**
- Inspired by Every's Compounding Engineering
- Built on BMAD planning methodology
- Voice system from HOLACE project

## Common Tasks

### Update Agent

```bash
# Edit the agent file
vi plugins/titanium-toolkit/agents/api-developer.md

# Test locally
/plugin uninstall titanium-toolkit@titanium-plugins
/plugin install titanium-toolkit@titanium-plugins

# Commit
git add plugins/titanium-toolkit/agents/api-developer.md
git commit -m "feat: Enhance api-developer agent with GraphQL support"
git push
```

### Add New Command

```bash
# Create command file
cat > plugins/titanium-toolkit/commands/new-command.md << 'EOF'
---
description: Brief description
---

# Command instructions for Claude
EOF

# Test and commit
git add plugins/titanium-toolkit/commands/new-command.md
git commit -m "feat: Add /new-command for [purpose]"
git push
```

### Fix Voice Hook Issue

```bash
# Edit the hook
vi plugins/titanium-toolkit/hooks/post_tool_use_elevenlabs.py

# Test manually
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"},"tool_response":{}}' | python3 plugins/titanium-toolkit/hooks/post_tool_use_elevenlabs.py

# Commit
git add plugins/titanium-toolkit/hooks/post_tool_use_elevenlabs.py
git commit -m "fix: Correct GPT-5 parameter usage in voice hook"
git push
```

## Maintenance Guidelines

1. **Keep dependencies updated**
   - Check for GPT-5 model updates
   - Monitor ElevenLabs API changes
   - Update MCP server recommendations

2. **Test before pushing**
   - Install plugin locally
   - Test all commands
   - Verify voice announcements work
   - Check agents are accessible

3. **Document changes**
   - Update README.md for user-facing changes
   - Update plugin README for plugin-specific updates
   - Keep CHANGELOG if adding one

4. **Security**
   - Never commit secrets
   - Review .gitignore regularly
   - Scan for accidentally committed keys

Remember: This marketplace showcases a unique voice-enhanced workflow that combines BMAD planning, Titanium implementation, compounding-engineering quality review, and Pieces context retention. Keep this integration story clear in all documentation.

# Titanium Toolkit

> Professional development toolkit with voice-enhanced AI workflows

## Overview

Titanium Toolkit is a comprehensive Claude Code plugin that enhances your development workflow with:

- **16 Specialized Builder Agents** - Implementation-focused agents for every development task
- **Voice Announcements** - Real-time audio feedback using ElevenLabs AI voices
- **Pieces Integration** - Seamless context recovery via `/catchup` command
- **GPT-5 Powered** - Ultra-fast summaries with GPT-5 nano and mini models

## Features

### Voice-Enhanced Development

Get real-time audio feedback as you code:

- **Tool Completions**: Hear "Created authentication module" after file operations
- **Session Summaries**: Get comprehensive overview when you finish: "I migrated 16 agents, updated voice hooks, and configured MCP servers"
- **Smart Notifications**: Context-aware alerts like "Permission needed for bash command"

Powered by:
- ElevenLabs "Sarah" voice (high quality)
- GPT-5 nano for quick 3-7 word summaries
- GPT-5 mini for detailed session analysis
- Automatic fallback to macOS voice if needed

### 16 Builder Agents

Access via `@agent-name`:

**Development:**
- `@api-developer` - Backend API development
- `@frontend-developer` - Modern frontend development
- `@devops-engineer` - CI/CD and deployment

**Quality:**
- `@code-reviewer` - Code review specialist
- `@debugger` - Error analysis and fixes
- `@test-runner` - Automated test execution
- `@tdd-specialist` - Test-driven development
- `@security-scanner` - Security vulnerability detection

**Documentation:**
- `@doc-writer` - Technical documentation
- `@api-documenter` - API documentation (OpenAPI/Swagger)

**Planning:**
- `@product-manager` - Requirements and user stories
- `@project-planner` - Project breakdown and planning
- `@meta-agent` - Creates new custom agents

**Specialized:**
- `@refactor` - Code refactoring specialist
- `@marketing-writer` - Marketing content
- `@shadcn-ui-builder` - UI/UX with shadcn components

### Slash Commands

**`/catchup`** - Query Pieces LTM for project context

Instantly resume work by querying your Pieces Long-Term Memory:
- Active projects from last 24-48 hours
- Recent file edits and commits
- Unfinished tasks and issues
- Current focus and priorities

Perfect for starting new Claude sessions without losing context.

## Prerequisites

### Required Software

- **Claude Code** 2.0.14+
- **Python** 3.11+
- **uv** (Python package manager) - https://docs.astral.sh/uv/
- **Node.js** 20+ (for MCP servers)

### Required API Keys

Add these to `~/.env`:

```bash
# Required for voice announcements
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

### Required MCP Servers

**IMPORTANT**: The Titanium Toolkit MCP server is automatically configured via the plugin's `.mcp.json` file. No manual installation needed!

The `tt` MCP server provides core BMAD document generation tools used by:
- `/titanium:plan` - Requirements to implementation plan
- `/bmad:start` - Complete BMAD workflow (Brief → PRD → Architecture → Epics)
- `/bmad:brief`, `/bmad:prd`, `/bmad:architecture`, `/bmad:epic` - Individual document generation

**Verify it's loaded**: After plugin installation, restart Claude Code and check:
```bash
# List MCP servers - you should see "tt" in the list
claude mcp list
```

If `tt` is missing, the plugin may not have loaded correctly. Try reinstalling the plugin.

### Recommended MCP Servers

**Pieces MCP** is highly recommended for the `/catchup` command:

For additional functionality, install these optional MCP servers:

```bash
# Optional but recommended
claude mcp add playwright --scope user --transport stdio -- npx @playwright/mcp@latest
claude mcp add pypi --scope user --transport stdio -- uvx pypi-query-mcp-server
claude mcp add vibe-check --scope user --transport stdio -- npx -y @pv-bhat/vibe-check-mcp start --stdio
```

**Note**: Pieces MCP requires Pieces OS to be running and the Pieces CLI to be installed:
```bash
pip3 install --upgrade pieces-cli
```

## Installation

### Via Plugin System

```bash
# Add the titanium-plugins marketplace
/plugin marketplace add webdevtodayjason/titanium-plugins

# Install the toolkit
/plugin install titanium-toolkit@webdevtodayjason/titanium-plugins
```

Restart Claude Code to activate.

### Verify Installation

```bash
# Check agents are available
@api-developer

# Test voice system (you should hear an announcement)
# Just use any Write or Edit tool

# Test Pieces integration
/catchup
```

## Usage

### Voice Announcements

Voice feedback works automatically:

**During Work:**
- File operations: "Created users.ts", "Updated API endpoints"
- Agent completions: "Test runner fixed failing tests"

**On Session End:**
- Comprehensive summary of what was accomplished
- Example: "I set up three MCP servers and configured voice announcements across all your projects"

**Notifications:**
- Alert sound (Tink) + voice message
- Context-aware: "Permission needed for bash command"

### Using Agents

Invoke any of the 16 builder agents via `@mention`:

```bash
# Code review
@code-reviewer

# Build an API
@api-developer Create REST endpoints for user management

# Frontend work
@frontend-developer Build a dashboard with shadcn components

# Testing
@test-runner Run all tests and fix failures
```

### Context Recovery

Start any new session with:

```bash
/catchup
```

Claude will query your Pieces LTM and provide:
- Active projects and recent work
- Files you were editing
- Unfinished tasks
- Current priorities

Perfect for resuming work after breaks or switching between projects.

## Configuration

### Customize Voice Settings

Edit the hook scripts in your global `~/.claude/hooks/`:

**Change voice:**
- Edit `elevenlabs_tts.py` line 61: `voice_id="EXAVITQu4vr4xnSDxMaL"`
- Find voices: https://elevenlabs.io/voice-library

**Adjust verbosity:**
- Edit `post_tool_use_elevenlabs.py` line 143: Add tools to skip list
- Current skips: TodoWrite, Grep, LS, Bash, Read, Glob, WebFetch, WebSearch

**Change models:**
- GPT-5 nano: `post_tool_use_elevenlabs.py` line 110
- GPT-5 mini: `stop.py` line 144

### Environment Variables

Required in `~/.env`:

```bash
# OpenAI (for GPT-5 summaries)
OPENAI_API_KEY=sk-proj-...

# ElevenLabs (for voice)
ELEVENLABS_API_KEY=sk_...
```

## Troubleshooting

### No voice announcements

1. Check API keys in `~/.env`
2. Verify `uv` is installed: `which uv`
3. Test ElevenLabs directly:
   ```bash
   uv run ~/.claude/hooks/utils/tts/elevenlabs_tts.py "test"
   ```
4. Check fallback works: `say "test"`

### /catchup not working

1. Verify Pieces is running: `ps aux | grep Pieces`
2. Check LTM is enabled in Pieces Desktop
3. Verify Pieces MCP: `claude mcp list`

### Agents not appearing

1. Restart Claude Code after installation
2. Check plugin is enabled: `/plugin`
3. Verify with `@` - agents should appear in autocomplete

## Development

### Local Testing

```bash
# Clone for development
git clone https://github.com/webdevtodayjason/titanium-plugins
cd titanium-plugins

# Test locally
/plugin marketplace add ./
/plugin install titanium-toolkit@titanium-plugins
```

### Modifying Voice Hooks

The voice system consists of:

1. **post_tool_use_elevenlabs.py** - Announces tool completions
2. **stop.py** - Session summaries
3. **notification.py** - User attention alerts
4. **subagent_stop.py** - Agent completion announcements

All use GPT-5 models + ElevenLabs for high-quality voice synthesis.

## Credits

Created by Jason Brashear ([Titanium Computing](https://titaniumcomputing.com))

**Inspired by and built upon:**
- [Every's Compounding Engineering](https://github.com/EveryInc/every-marketplace) - Workflow methodology and agent patterns
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) - Requirements and planning framework
- HOLACE project - Voice system architecture

Special thanks to the Every team and BMAD community for pioneering AI-enhanced development workflows.

## License

MIT License - See LICENSE file for details

# Titanium Clawdbot Plugins

Custom Clawdbot plugins for Titanium Computing. These plugins enforce best practices and behavioral patterns for the Argent assistant.

## Plugins

### 1. Summarize TTS Enforcer

**ID:** `summarize-tts-enforcer`  
**Purpose:** Forces voice output when the `summarize` tool is used

**What it does:**
- Intercepts `summarize` tool results
- Appends mandatory instructions to use `sag` (ElevenLabs TTS)
- Prevents text-dumping of summaries

**Installation:**
```bash
# Link to workspace hooks (per-agent)
ln -s /Users/sem/titanium-plugins/clawdbot-plugins/summarize-tts-enforcer \
      ~/clawd/.clawdbot/extensions/summarize-tts-enforcer

# Or link to global extensions (all workspaces)
ln -s /Users/sem/titanium-plugins/clawdbot-plugins/summarize-tts-enforcer \
      ~/.clawdbot/extensions/summarize-tts-enforcer

# Enable the plugin
clawdbot plugins enable summarize-tts-enforcer

# Restart gateway
clawdbot gateway restart
```

**Configuration:**
```json
{
  "plugins": {
    "entries": {
      "summarize-tts-enforcer": {
        "enabled": true,
        "config": {
          "voice": "cgSgspJ2msm6clMCkdW9"  // Jessica voice ID (default)
        }
      }
    }
  }
}
```

---

### 2. Canvas Documentation Enforcer

**ID:** `canvas-docs-enforcer`  
**Purpose:** Forces canvas usage for documentation tasks instead of inline markdown

**What it does:**
- Injects enforcement rules at agent bootstrap
- Detects documentation keywords
- Reminds the agent to use `canvas` for proper presentation

**Installation:**
```bash
# Link to workspace extensions (per-agent)
ln -s /Users/sem/titanium-plugins/clawdbot-plugins/canvas-docs-enforcer \
      ~/clawd/.clawdbot/extensions/canvas-docs-enforcer

# Or link to global extensions (all workspaces)
ln -s /Users/sem/titanium-plugins/clawdbot-plugins/canvas-docs-enforcer \
      ~/.clawdbot/extensions/canvas-docs-enforcer

# Enable the plugin
clawdbot plugins enable canvas-docs-enforcer

# Restart gateway
clawdbot gateway restart
```

**Configuration:**
```json
{
  "plugins": {
    "entries": {
      "canvas-docs-enforcer": {
        "enabled": true,
        "config": {
          "docKeywords": [
            "documentation",
            "guide",
            "tutorial",
            "reference",
            "manual",
            "readme",
            "wiki",
            "spec",
            "specification"
          ]
        }
      }
    }
  }
}
```

---

## Development

### Creating New Plugins

1. Create directory: `clawdbot-plugins/<plugin-name>/`
2. Add files:
   - `clawdbot.plugin.json` - Plugin metadata
   - `index.ts` - Plugin implementation
   - `package.json` - NPM metadata

3. Register hooks in `index.ts`:
```typescript
import type { ClawdbotPluginApi } from "...";

export default function register(api: ClawdbotPluginApi) {
  api.registerHook("event:type", (context) => {
    // Your logic here
  });
}
```

### Testing Plugins

```bash
# List discovered plugins
clawdbot plugins list

# Check plugin info
clawdbot plugins info <plugin-id>

# Enable/disable
clawdbot plugins enable <plugin-id>
clawdbot plugins disable <plugin-id>

# View gateway logs
tail -f ~/.clawdbot/gateway.log
```

---

## Distribution

### Publishing to GitHub

```bash
cd /Users/sem/titanium-plugins
git add clawdbot-plugins/
git commit -m "Add enforcement plugins"
git push origin main
```

### Installing from Git

```bash
clawdbot plugins install https://github.com/titaniumcomputing/titanium-plugins/clawdbot-plugins/summarize-tts-enforcer
clawdbot plugins install https://github.com/titaniumcomputing/titanium-plugins/clawdbot-plugins/canvas-docs-enforcer
```

---

## License

MIT License - See individual plugin directories for details.

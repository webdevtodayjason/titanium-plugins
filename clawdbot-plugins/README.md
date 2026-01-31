# Titanium Clawdbot Plugins

Custom Clawdbot plugins for Titanium Computing. These plugins enforce best practices and behavioral patterns for the Argent assistant.

## 🚨 Important: Two Types of Enforcement

### Weak Enforcement (Prompts)
- `summarize-tts-enforcer` - Modifies tool results
- `canvas-docs-enforcer` - Injects instructions
- **Problem:** Agent can still ignore these

### Strong Enforcement (Blocking)
- `response-validator` - **BLOCKS messages** that violate rules
- **Solution:** Uses `message_sending` hook to prevent bad responses from reaching you

## Plugins

### 1. ⚡ Response Validator (RECOMMENDED)

**ID:** `response-validator`  
**Purpose:** Actually BLOCKS responses that violate formatting rules

**What it enforces:**
1. **Report requests** → Must use `Write` + `canvas` tools
2. **Documentation** → Must use `canvas` for presentation
3. **Audio mode** → Long responses must use TTS
4. **Long structured content** → Must use canvas

**How it works:**
- Uses `api.on('message_sending')` hook
- Runs BEFORE message is sent
- Returns `{ cancel: true }` to block violations
- Forces agent to retry with correct tooling

**Installation:**
```bash
clawdbot plugins install /Users/sem/titanium-plugins/clawdbot-plugins/response-validator
clawdbot gateway restart
```

**Configuration:**
```json
{
  "plugins": {
    "entries": {
      "response-validator": {
        "enabled": true,
        "config": {
          "reportKeywords": ["report", "document", "write up", "summarize to file"],
          "docKeywords": ["documentation", "guide", "tutorial", "spec"],
          "audioMaxLength": 300,
          "enabledChannels": ["webchat"],  // Only enforce in dashboard
          "logContext": false               // Enable to debug channel detection
        }
      }
    }
  }
}
```

**Channel Options:**
- `["webchat"]` - Only Argent dashboard (default)
- `["*"]` - All channels (TUI, Discord, Telegram, etc.)
- `["webchat", "discord"]` - Specific channels only
- `[]` - Disabled everywhere

**Testing:**
```bash
# Should be blocked (no Write tool)
"Give me a report on X"

# Should be allowed (uses Write + canvas)
"Give me a report on X" → agent calls Write, then canvas

# Should be blocked if audio enabled
Long response without TTS when [AUDIO_ENABLED]
```

---

### 2. Summarize TTS Enforcer (DEPRECATED)

**ID:** `summarize-tts-enforcer`  
**Purpose:** Forces voice output when the `summarize` tool is used

**What it does:**
- Intercepts `summarize` tool results
- Appends mandatory instructions to use `sag` (ElevenLabs TTS)
- Prevents text-dumping of summaries

**Installation:**
```bash
# Install from local path
clawdbot plugins install /Users/sem/titanium-plugins/clawdbot-plugins/summarize-tts-enforcer

# Plugins are enabled by default after install
# Restart gateway to load
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
# Install from local path
clawdbot plugins install /Users/sem/titanium-plugins/clawdbot-plugins/canvas-docs-enforcer

# Plugins are enabled by default after install
# Restart gateway to load
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

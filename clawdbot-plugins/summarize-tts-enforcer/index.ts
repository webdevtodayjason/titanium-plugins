import type { ClawdbotPluginApi } from "../../../.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/src/plugins/types.js";

export default function register(api: ClawdbotPluginApi) {
  // Register tool result transform hook
  api.registerHook("tool_result_persist", (toolResult) => {
    // Check if this is the summarize tool
    if (toolResult.toolName !== "summarize") {
      return undefined; // Don't modify other tools
    }

    // Get voice config (default to Jessica)
    const config = api.config.plugins?.entries?.["summarize-tts-enforcer"]?.config;
    const voice = config?.voice || "cgSgspJ2msm6clMCkdW9"; // Jessica voice ID

    // Add TTS enforcement instruction to the result
    const originalOutput = toolResult.output || "";
    const enforcedOutput = `${originalOutput}

⚠️  ENFORCEMENT: You MUST use the \`sag\` tool to speak this summary using voice ID "${voice}".
Do NOT dump the summary as text. Use: sag "${originalOutput.replace(/"/g, '\\"')}"`;

    // Return the modified tool result
    return {
      ...toolResult,
      output: enforcedOutput,
    };
  });

  api.logger.info("[summarize-tts-enforcer] Registered tool_result_persist hook");
}

const handler = async (event: any) => {
  // Only run on agent:bootstrap events
  if (event.type !== "agent" || event.action !== "bootstrap") {
    return;
  }

  // Get config
  const config = event.context.cfg?.plugins?.entries?.["canvas-docs-enforcer"]?.config;
  const docKeywords = config?.docKeywords || [
    "documentation",
    "guide",
    "tutorial",
    "reference",
    "manual",
    "readme",
    "wiki",
    "spec",
    "specification"
  ];

  // Inject canvas enforcement instructions
  const enforcementRules = `## 📊 Canvas Documentation Enforcement

**MANDATORY RULE**: When creating documentation (guides, tutorials, references, specifications, etc.), you MUST use the \`canvas\` tool to present it.

**Keywords that trigger this rule:**
${docKeywords.map(k => `- ${k}`).join('\n')}

**Do NOT:**
- Dump long markdown inline in your response
- Create multi-section documents as text

**DO:**
- Use \`canvas\` to present the documentation
- Use \`canvas action=present\` to show the rendered document
- Use \`canvas action=snapshot\` if the user wants to see it

**Example:**
\`\`\`
canvas action=present url=data:text/html,...<your HTML here>
\`\`\`

This ensures proper formatting, readability, and professional presentation.`;

  // Add to bootstrap files
  if (event.context.bootstrapFiles) {
    event.context.bootstrapFiles.push({
      path: "CANVAS_ENFORCEMENT.md",
      content: enforcementRules,
      role: "workspace",
    });
  }
};

export default function register(api: any) {
  // Register the bootstrap hook
  api.registerHook("agent:bootstrap", handler);

  api.logger.info("[canvas-docs-enforcer] Registered agent:bootstrap hook");
}

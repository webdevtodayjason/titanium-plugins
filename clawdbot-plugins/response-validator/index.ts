export default function register(api: any) {
  // Get config with defaults
  const getConfig = () => {
    const config = api.config?.plugins?.entries?.["response-validator"]?.config || {};
    return {
      reportKeywords: config.reportKeywords || [
        "report", "document", "write up", "write-up", "create a report", "summarize to file"
      ],
      docKeywords: config.docKeywords || [
        "documentation", "guide", "tutorial", "reference", "manual", 
        "readme", "wiki", "spec", "specification"
      ],
      audioMaxLength: config.audioMaxLength || 300
    };
  };

  // Register message_sending hook (runs BEFORE message is sent, can BLOCK)
  api.on('message_sending', async (event: any, ctx: any) => {
    const userMsg = ctx?.triggeringMessage?.text || ctx?.originalMessage?.text || '';
    const response = event.content?.text || event.text || '';
    const toolCalls = ctx?.toolCalls || [];
    const audioEnabled = ctx?.session?.audioEnabled || ctx?.audioEnabled;
    
    const config = getConfig();
    const toolNames = toolCalls.map((t: any) => t.name || t.tool || t.toolName);

    // Rule 1: Report/Document Detection
    const isReportRequest = config.reportKeywords.some((kw: string) => 
      new RegExp(`\\b${kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i').test(userMsg)
    );

    if (isReportRequest) {
      const hasWrite = toolNames.includes('Write') || toolNames.includes('write');
      const hasCanvas = toolNames.includes('canvas');

      if (!hasWrite || !hasCanvas) {
        api.logger.warn('[response-validator] BLOCKED: Report request missing Write or canvas');
        api.logger.warn(`  User message: ${userMsg.substring(0, 100)}...`);
        api.logger.warn(`  Tool calls: ${toolNames.join(', ')}`);
        
        // BLOCK THE MESSAGE
        return {
          cancel: true,
          error: '❌ VALIDATION FAILED: Report requests require:\n1. Write tool (create file)\n2. canvas tool (present it)\n3. Brief summary in response'
        };
      }
    }

    // Rule 2: Documentation Detection
    const isDocRequest = config.docKeywords.some((kw: string) => 
      new RegExp(`\\b${kw}\\b`, 'i').test(userMsg)
    );

    if (isDocRequest && response.length > 500) {
      const hasCanvas = toolNames.includes('canvas');
      
      if (!hasCanvas) {
        api.logger.warn('[response-validator] BLOCKED: Documentation without canvas');
        
        return {
          cancel: true,
          error: '❌ VALIDATION FAILED: Documentation must use canvas for presentation'
        };
      }
    }

    // Rule 3: Audio Length Check
    if (audioEnabled && response.length > config.audioMaxLength) {
      const hasTTS = toolNames.includes('tts') || toolNames.includes('sag');
      
      if (!hasTTS) {
        api.logger.warn('[response-validator] BLOCKED: Audio response too long without TTS');
        api.logger.warn(`  Response length: ${response.length} (max: ${config.audioMaxLength})`);
        
        return {
          cancel: true,
          error: `❌ VALIDATION FAILED: Audio enabled - response is ${response.length} chars (max: ${config.audioMaxLength})\nMust use TTS tool or shorten response`
        };
      }
    }

    // Rule 4: Long responses without structure
    if (response.length > 1000 && !toolNames.includes('canvas')) {
      const hasMultipleSections = (response.match(/^#+\s/gm) || []).length > 3;
      
      if (hasMultipleSections) {
        api.logger.warn('[response-validator] BLOCKED: Long structured content without canvas');
        
        return {
          cancel: true,
          error: '❌ VALIDATION FAILED: Long structured content should use canvas for better presentation'
        };
      }
    }

    // Allow message
    return { cancel: false };
  }, { priority: 100 }); // High priority to run early

  api.logger.info('[response-validator] Response validator registered (message_sending hook)');
}

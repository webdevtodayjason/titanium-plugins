#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///

import argparse
import json
import os
import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!"
    ]


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys and MCP.
    Priority order: ElevenLabs MCP > OpenAI > local
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs MCP first (highest priority)
    elevenlabs_mcp_script = tts_dir / "elevenlabs_mcp.py"
    if elevenlabs_mcp_script.exists():
        return str(elevenlabs_mcp_script)
    
    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # Fall back to local TTS (no API key required)
    local_script = tts_dir / "local_tts.py"
    if local_script.exists():
        return str(local_script)
    
    return None


def get_session_summary(transcript_path):
    """
    Analyze the transcript and create a comprehensive summary
    of what Claude accomplished in this session.

    Uses GPT-5 mini for intelligent session summarization.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not transcript_path or not os.path.exists(transcript_path):
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Read transcript and collect tool uses
        tool_uses = []
        user_requests = []

        with open(transcript_path, 'r') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())

                    # Collect user messages
                    if msg.get('role') == 'user':
                        content = msg.get('content', '')
                        if isinstance(content, str) and content.strip():
                            user_requests.append(content[:100])  # First 100 chars

                    # Collect tool uses from content blocks
                    if msg.get('role') == 'assistant':
                        content = msg.get('content', [])
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get('type') == 'tool_use':
                                    tool_uses.append({
                                        'name': block.get('name'),
                                        'input': block.get('input', {})
                                    })
                except:
                    pass

        if not tool_uses:
            return None

        # Build context from tools and user intent
        context = f"Session completed with {len(tool_uses)} operations.\n"

        if user_requests:
            context += f"User requested: {user_requests[0]}\n\n"

        context += "Key actions:\n"

        # Summarize tool usage
        tool_counts = {}
        for tool in tool_uses:
            name = tool['name']
            tool_counts[name] = tool_counts.get(name, 0) + 1

        for tool_name, count in list(tool_counts.items())[:10]:
            context += f"- {tool_name}: {count}x\n"

        prompt = f"""Summarize what Claude accomplished in this work session in 1-2 natural sentences for a voice announcement.
Focus on the end result and key accomplishments, not individual steps.
Be conversational and speak directly to the user in first person (I did...).
Keep it concise but informative.

{context}

Examples of good summaries:
- "I set up three MCP servers and configured voice announcements across all your projects"
- "I migrated your HOLACE configuration globally and everything is ready to use"
- "I fixed all the failing tests and updated the authentication module"
- "I created the payment integration with Stripe and added webhook handling"

Summary:"""

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=100,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Session summary error: {e}", file=sys.stderr)
        return None


def get_llm_completion_message():
    """
    Generate completion message using available LLM services.
    Priority order: OpenAI > Anthropic > fallback to random message
    
    Returns:
        str: Generated or fallback completion message
    """
    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"
    
    # Try OpenAI first (highest priority)
    if os.getenv('OPENAI_API_KEY'):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(oai_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Try Anthropic second
    if os.getenv('ANTHROPIC_API_KEY'):
        anth_script = llm_dir / "anth.py"
        if anth_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(anth_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)

def announce_completion(input_data):
    """Announce completion with comprehensive session summary."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Try to get comprehensive session summary from transcript
        transcript_path = input_data.get('transcript_path')
        completion_message = get_session_summary(transcript_path)

        # Fallback to generic message if summary fails
        if not completion_message:
            completion_message = get_llm_completion_message()

        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ],
        capture_output=True,  # Suppress output
        timeout=15  # Longer timeout for longer summaries
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "stop.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    chat_file = os.path.join(log_dir, 'chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # Fail silently

        # Announce completion via TTS
        announce_completion(input_data)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
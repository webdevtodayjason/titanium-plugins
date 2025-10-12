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
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs (highest priority for quality)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "local_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def get_smart_notification(message, input_data):
    """
    Use GPT-5 nano to generate context-aware notification message.
    Analyzes recent transcript to understand what Claude needs.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Extract any additional context
        context = f"Notification: {message}\n"

        # Add fields from input_data
        for key in ['status', 'reason', 'permission_mode', 'cwd']:
            if input_data.get(key):
                context += f"{key}: {input_data[key]}\n"

        # Try to get recent context from transcript if available
        transcript_path = input_data.get('transcript_path')
        if transcript_path and os.path.exists(transcript_path):
            try:
                # Read last few messages to understand context
                with open(transcript_path, 'r') as f:
                    lines = f.readlines()
                    last_lines = lines[-10:] if len(lines) > 10 else lines

                    for line in reversed(last_lines):
                        try:
                            msg = json.loads(line.strip())
                            # Look for recent user message
                            if msg.get('role') == 'user':
                                user_msg = msg.get('content', '')
                                if isinstance(user_msg, str):
                                    context += f"Last user request: {user_msg[:100]}\n"
                                    break
                        except:
                            pass
            except:
                pass

        prompt = f"""Create a brief 4-8 word voice notification that tells the user what Claude is waiting for.
Be specific about what action, permission, or input is needed.

{context}

Examples:
- "Waiting for edit approval"
- "Need permission for bash command"
- "Ready for your response"
- "Waiting to continue your task"

Notification:"""

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=20,
        )

        return response.choices[0].message.content.strip().strip('"').strip("'")

    except Exception as e:
        print(f"Smart notification error: {e}", file=sys.stderr)
        return None


def get_notification_message(message, input_data=None):
    """
    Convert notification message to a more natural spoken version.
    """
    # Try smart notification first for "waiting" messages
    if ("waiting" in message.lower() or "idle" in message.lower()) and input_data:
        smart_msg = get_smart_notification(message, input_data)
        if smart_msg:
            return smart_msg

    # Common notification transformations
    if "permission" in message.lower():
        # Extract tool name if present
        if "to use" in message.lower():
            parts = message.split("to use")
            if len(parts) > 1:
                tool_name = parts[1].strip().rstrip('.')
                return f"Permission needed for {tool_name}"
        return "Claude needs your permission"

    elif "waiting for your input" in message.lower():
        # More informative default if smart notification failed
        return "Waiting for your response"

    elif "idle" in message.lower():
        return "Claude is ready"

    # Default: use the message as-is but make it more concise
    # Remove "Claude" from beginning if present
    if message.startswith("Claude "):
        message = message[7:]

    # Truncate very long messages
    if len(message) > 50:
        message = message[:47] + "..."

    return message


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract notification message
        message = input_data.get("message", "")
        
        if not message:
            sys.exit(0)

        # Convert to natural speech with context
        spoken_message = get_notification_message(message, input_data)

        # Use ElevenLabs for consistent voice across all hooks
        script_dir = Path(__file__).parent
        elevenlabs_script = script_dir / "utils" / "tts" / "elevenlabs_tts.py"

        try:
            subprocess.run(["afplay", "/System/Library/Sounds/Tink.aiff"], timeout=1)
            subprocess.run(
                ["uv", "run", str(elevenlabs_script), spoken_message],
                capture_output=True,
                timeout=10
            )
        except Exception:
            pass
        
        # Optional: Also use system notification if available
        try:
            # Try notify-send on Linux
            subprocess.run([
                "notify-send", "-a", "Claude Code", "Claude Code", message
            ], capture_output=True, timeout=2)
        except:
            try:
                # Try osascript on macOS
                subprocess.run([
                    "osascript", "-e", 
                    f'display notification "{message}" with title "Claude Code"'
                ], capture_output=True, timeout=2)
            except:
                pass  # No system notification available
        
        # Log for debugging (optional)
        log_dir = os.path.join(os.getcwd(), "logs")
        if os.path.exists(log_dir):
            log_path = os.path.join(log_dir, "notifications.json")
            try:
                logs = []
                if os.path.exists(log_path):
                    with open(log_path, 'r') as f:
                        logs = json.load(f)
                
                logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "message": message,
                    "spoken": spoken_message
                })
                
                # Keep last 50 entries
                logs = logs[-50:]
                
                with open(log_path, 'w') as f:
                    json.dump(logs, f, indent=2)
            except:
                pass
        
        sys.exit(0)
        
    except Exception:
        # Fail silently
        sys.exit(0)


if __name__ == "__main__":
    main()
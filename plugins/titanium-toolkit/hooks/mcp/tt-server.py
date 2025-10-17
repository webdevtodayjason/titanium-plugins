#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp>=1.0.0",
#     "python-dotenv",
# ]
# ///

"""
Titanium Toolkit MCP Server

Exposes utility scripts as MCP tools for Claude Code.

Available Tools:
- plan_parser: Parse requirements into implementation plan
- bmad_generator: Generate BMAD documents (brief, PRD, architecture, epic, index, research)
- bmad_validator: Validate BMAD documents

Usage:
    This server is automatically registered when the titanium-toolkit plugin is installed.
    Tools are accessible as: mcp__plugin_titanium-toolkit_tt__<tool_name>
"""

import asyncio
import subprocess
import sys
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent


# Initialize MCP server
server = Server("tt")

# Get the plugin root directory (3 levels up from this file)
PLUGIN_ROOT = Path(__file__).parent.parent.parent
UTILS_DIR = PLUGIN_ROOT / "hooks" / "utils"


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available Titanium Toolkit utility tools."""
    return [
        Tool(
            name="plan_parser",
            description="Parse requirements into structured implementation plan with epics, stories, tasks, and agent assignments",
            inputSchema={
                "type": "object",
                "properties": {
                    "requirements_file": {
                        "type": "string",
                        "description": "Path to requirements file (e.g., '.titanium/requirements.md')"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Absolute path to project directory (e.g., '$(pwd)')"
                    }
                },
                "required": ["requirements_file", "project_path"]
            }
        ),
        Tool(
            name="bmad_generator",
            description="Generate BMAD documents (brief, prd, architecture, epic, index, research) using GPT-4",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["brief", "prd", "architecture", "epic", "index", "research"],
                        "description": "Type of BMAD document to generate"
                    },
                    "input_path": {
                        "type": "string",
                        "description": "Path to input file or directory (depends on doc_type)"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Absolute path to project directory"
                    }
                },
                "required": ["doc_type", "input_path", "project_path"]
            }
        ),
        Tool(
            name="bmad_validator",
            description="Validate BMAD documents for completeness and quality",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["brief", "prd", "architecture", "epic"],
                        "description": "Type of BMAD document to validate"
                    },
                    "document_path": {
                        "type": "string",
                        "description": "Path to BMAD document to validate"
                    }
                },
                "required": ["doc_type", "document_path"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a Titanium Toolkit utility tool."""

    try:
        if name == "plan_parser":
            return await run_plan_parser(arguments)
        elif name == "bmad_generator":
            return await run_bmad_generator(arguments)
        elif name == "bmad_validator":
            return await run_bmad_validator(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def run_plan_parser(args: dict[str, Any]) -> list[TextContent]:
    """Run the plan_parser.py utility."""
    requirements_file = args["requirements_file"]
    project_path = args["project_path"]

    script_path = UTILS_DIR / "workflow" / "plan_parser.py"

    # Validate script exists
    if not script_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: plan_parser.py not found at {script_path}"
        )]

    # Run the script
    result = subprocess.run(
        ["uv", "run", str(script_path), requirements_file, project_path],
        capture_output=True,
        text=True,
        cwd=project_path
    )

    if result.returncode != 0:
        error_msg = f"Error running plan_parser:\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return [TextContent(type="text", text=error_msg)]

    # Return the plan JSON
    return [TextContent(
        type="text",
        text=f"✅ Plan generated successfully!\n\nPlan saved to: {project_path}/.titanium/plan.json\n\n{result.stdout}"
    )]


async def run_bmad_generator(args: dict[str, Any]) -> list[TextContent]:
    """Run the bmad_generator.py utility."""
    doc_type = args["doc_type"]
    input_path = args["input_path"]
    project_path = args["project_path"]

    script_path = UTILS_DIR / "bmad" / "bmad_generator.py"

    # Validate script exists
    if not script_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: bmad_generator.py not found at {script_path}"
        )]

    # Run the script
    result = subprocess.run(
        ["uv", "run", str(script_path), doc_type, input_path, project_path],
        capture_output=True,
        text=True,
        cwd=project_path
    )

    if result.returncode != 0:
        error_msg = f"Error running bmad_generator:\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return [TextContent(type="text", text=error_msg)]

    # Return success message with output
    return [TextContent(
        type="text",
        text=f"✅ BMAD {doc_type} generated successfully!\n\n{result.stdout}"
    )]


async def run_bmad_validator(args: dict[str, Any]) -> list[TextContent]:
    """Run the bmad_validator.py utility."""
    doc_type = args["doc_type"]
    document_path = args["document_path"]

    script_path = UTILS_DIR / "bmad" / "bmad_validator.py"

    # Validate script exists
    if not script_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: bmad_validator.py not found at {script_path}"
        )]

    # Get the document's parent directory as working directory
    document_parent = Path(document_path).parent

    # Run the script
    result = subprocess.run(
        ["uv", "run", str(script_path), doc_type, document_path],
        capture_output=True,
        text=True,
        cwd=str(document_parent)
    )

    # Validator returns non-zero for validation failures (expected behavior)
    # Only treat it as an error if there's stderr output (actual script error)
    if result.returncode != 0 and result.stderr and "Traceback" in result.stderr:
        error_msg = f"Error running bmad_validator:\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return [TextContent(type="text", text=error_msg)]

    # Return validation results (includes both pass and fail cases)
    return [TextContent(
        type="text",
        text=f"BMAD {doc_type} validation results:\n\n{result.stdout}"
    )]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

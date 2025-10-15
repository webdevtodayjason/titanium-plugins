#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "openai",
# ]
# ///

"""
Plan Parser Utility

Uses GPT-4 to break down requirements into structured implementation plans.
Creates .titanium/plan.json with epics, stories, tasks, and agent assignments.

Usage:
    uv run plan_parser.py <requirements_file> <project_path>

Example:
    uv run plan_parser.py .titanium/requirements.md "$(pwd)"

Output:
    - Creates .titanium/plan.json with structured plan
    - Prints JSON to stdout
"""

import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


def parse_requirements_to_plan(requirements_text: str, project_path: str) -> dict:
    """
    Use GPT-4 to break down requirements into structured plan.

    Args:
        requirements_text: Requirements document text
        project_path: Absolute path to project directory

    Returns:
        Structured plan dictionary with epics, stories, tasks
    """
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables", file=sys.stderr)
        print("Please add your OpenAI API key to ~/.env file:", file=sys.stderr)
        print("OPENAI_API_KEY=sk-your-key-here", file=sys.stderr)
        sys.exit(1)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except ImportError:
        print("Error: openai package not installed", file=sys.stderr)
        print("This should be handled by uv automatically.", file=sys.stderr)
        sys.exit(1)

    # Build GPT-4 prompt
    prompt = f"""Analyze these requirements and create a structured implementation plan.

Requirements:
{requirements_text}

Create a JSON plan with this exact structure:
{{
  "epics": [
    {{
      "name": "Epic name",
      "description": "Epic description",
      "stories": [
        {{
          "name": "Story name",
          "description": "User story or technical description",
          "tasks": [
            {{
              "name": "Task name",
              "agent": "@agent-name",
              "estimated_time": "30m",
              "dependencies": []
            }}
          ]
        }}
      ]
    }}
  ],
  "agents_needed": ["@api-developer", "@frontend-developer"],
  "estimated_total_time": "4h"
}}

Available agents to use:
- @product-manager: Requirements validation, clarification, acceptance criteria
- @api-developer: Backend APIs (REST/GraphQL), database, authentication
- @frontend-developer: UI/UX, React/Vue/etc, responsive design
- @devops-engineer: CI/CD, deployment, infrastructure, Docker/K8s
- @test-runner: Running tests, test execution, test reporting
- @tdd-specialist: Writing tests, test-driven development, test design
- @code-reviewer: Code review, best practices, code quality
- @security-scanner: Security vulnerabilities, security best practices
- @doc-writer: Technical documentation, API docs, README files
- @api-documenter: OpenAPI/Swagger specs, API documentation
- @debugger: Debugging, error analysis, troubleshooting
- @refactor: Code refactoring, code improvement, tech debt
- @project-planner: Project breakdown, task planning, estimation
- @shadcn-ui-builder: UI components using shadcn/ui library
- @meta-agent: Creating new custom agents

Guidelines:
1. Break down into logical epics (major features)
2. Each epic should have 1-5 stories
3. Each story should have 2-10 tasks
4. Assign the most appropriate agent to each task
5. Estimate time realistically (15m, 30m, 1h, 2h, etc.)
6. List dependencies between tasks (use task names)
7. Start with @product-manager for requirements validation
8. Always include @test-runner or @tdd-specialist for testing
9. Consider @security-scanner for auth/payment/sensitive features
10. End with @doc-writer for documentation

Return ONLY valid JSON, no markdown code blocks, no explanations."""

    try:
        # Call GPT-4
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.3  # Lower temperature for more deterministic planning
        )

        plan_json = response.choices[0].message.content.strip()

        # Clean up markdown code blocks if present
        if plan_json.startswith("```json"):
            plan_json = plan_json[7:]
        if plan_json.startswith("```"):
            plan_json = plan_json[3:]
        if plan_json.endswith("```"):
            plan_json = plan_json[:-3]
        plan_json = plan_json.strip()

        # Parse and validate JSON
        plan = json.loads(plan_json)

        # Validate structure
        if "epics" not in plan:
            raise ValueError("Plan missing 'epics' field")
        if "agents_needed" not in plan:
            raise ValueError("Plan missing 'agents_needed' field")
        if "estimated_total_time" not in plan:
            raise ValueError("Plan missing 'estimated_total_time' field")

        # Save plan to file
        plan_path = Path(project_path) / ".titanium" / "plan.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write
        temp_path = plan_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(plan, f, indent=2)
        temp_path.replace(plan_path)

        return plan

    except json.JSONDecodeError as e:
        print(f"Error: GPT-4 returned invalid JSON: {e}", file=sys.stderr)
        print(f"Response was: {plan_json[:200]}...", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error calling GPT-4: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """CLI interface for plan parsing."""

    if len(sys.argv) < 3:
        print("Usage: plan_parser.py <requirements_file> <project_path>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  uv run plan_parser.py .titanium/requirements.md \"$(pwd)\"", file=sys.stderr)
        sys.exit(1)

    requirements_file = sys.argv[1]
    project_path = sys.argv[2]

    # Validate requirements file exists
    if not Path(requirements_file).exists():
        print(f"Error: Requirements file not found: {requirements_file}", file=sys.stderr)
        sys.exit(1)

    # Read requirements
    try:
        with open(requirements_file, 'r') as f:
            requirements_text = f.read()
    except Exception as e:
        print(f"Error reading requirements file: {e}", file=sys.stderr)
        sys.exit(1)

    if not requirements_text.strip():
        print("Error: Requirements file is empty", file=sys.stderr)
        sys.exit(1)

    # Parse requirements to plan
    plan = parse_requirements_to_plan(requirements_text, project_path)

    # Output plan to stdout
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()

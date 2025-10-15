#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Workflow State Management Utility

Manages workflow state via file-based JSON storage in .titanium/workflow-state.json

Commands:
    init <project_path> <workflow_type> <goal>     Initialize new workflow
    update_phase <project_path> <phase> <status>   Update current phase
    get <project_path>                              Get current state
    complete <project_path>                         Mark workflow complete

Examples:
    uv run workflow_state.py init "$(pwd)" "development" "Implement user auth"
    uv run workflow_state.py update_phase "$(pwd)" "implementation" "in_progress"
    uv run workflow_state.py get "$(pwd)"
    uv run workflow_state.py complete "$(pwd)"
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Constants
STATE_FILE = ".titanium/workflow-state.json"


def init_workflow(project_path: str, workflow_type: str, goal: str) -> dict:
    """
    Initialize a new workflow state file.

    Args:
        project_path: Absolute path to project directory
        workflow_type: Type of workflow (development, bug-fix, refactor, review)
        goal: User's stated goal for this workflow

    Returns:
        Initial state dictionary
    """
    state_path = Path(project_path) / STATE_FILE
    state_path.parent.mkdir(parents=True, exist_ok=True)

    state = {
        "workflow_type": workflow_type,
        "goal": goal,
        "status": "planning",
        "started_at": datetime.now().isoformat(),
        "current_phase": "planning",
        "phases": [],
        "completed_tasks": [],
        "pending_tasks": []
    }

    # Atomic write
    temp_path = state_path.with_suffix('.tmp')
    with open(temp_path, 'w') as f:
        json.dump(state, f, indent=2)
    temp_path.replace(state_path)

    return state


def update_phase(project_path: str, phase_name: str, status: str = "in_progress") -> dict:
    """
    Update current workflow phase.

    Args:
        project_path: Absolute path to project directory
        phase_name: Name of phase (planning, implementation, review, completed)
        status: Status of phase (in_progress, completed, failed)

    Returns:
        Updated state dictionary or None if state doesn't exist
    """
    state_path = Path(project_path) / STATE_FILE

    if not state_path.exists():
        print(f"Error: No workflow state found at {state_path}", file=sys.stderr)
        return None

    # Read current state
    with open(state_path, 'r') as f:
        state = json.load(f)

    # Update current phase and status
    state["current_phase"] = phase_name
    state["status"] = status

    # Create phase entry
    phase_entry = {
        "name": phase_name,
        "status": status,
        "started_at": datetime.now().isoformat()
    }

    if status == "completed":
        phase_entry["completed_at"] = datetime.now().isoformat()

    # Update or add phase
    phase_exists = False
    for i, p in enumerate(state["phases"]):
        if p["name"] == phase_name:
            state["phases"][i] = {**p, **phase_entry}
            phase_exists = True
            break

    if not phase_exists:
        state["phases"].append(phase_entry)

    # Atomic write
    temp_path = state_path.with_suffix('.tmp')
    with open(temp_path, 'w') as f:
        json.dump(state, f, indent=2)
    temp_path.replace(state_path)

    return state


def get_state(project_path: str) -> dict:
    """
    Get current workflow state.

    Args:
        project_path: Absolute path to project directory

    Returns:
        State dictionary or None if state doesn't exist
    """
    state_path = Path(project_path) / STATE_FILE

    if not state_path.exists():
        return None

    with open(state_path, 'r') as f:
        return json.load(f)


def complete_workflow(project_path: str) -> dict:
    """
    Mark workflow as complete.

    Args:
        project_path: Absolute path to project directory

    Returns:
        Updated state dictionary or None if state doesn't exist
    """
    state_path = Path(project_path) / STATE_FILE

    if not state_path.exists():
        print(f"Error: No workflow state found at {state_path}", file=sys.stderr)
        return None

    # Read current state
    with open(state_path, 'r') as f:
        state = json.load(f)

    # Update to completed
    state["status"] = "completed"
    state["current_phase"] = "completed"
    state["completed_at"] = datetime.now().isoformat()

    # Mark current phase as completed if it exists
    if state["phases"]:
        for phase in state["phases"]:
            if phase["status"] == "in_progress":
                phase["status"] = "completed"
                phase["completed_at"] = datetime.now().isoformat()

    # Atomic write
    temp_path = state_path.with_suffix('.tmp')
    with open(temp_path, 'w') as f:
        json.dump(state, f, indent=2)
    temp_path.replace(state_path)

    return state


def main():
    """CLI interface for workflow state management."""

    if len(sys.argv) < 3:
        print("Usage: workflow_state.py <command> <project_path> [args...]", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  init <project_path> <workflow_type> <goal>", file=sys.stderr)
        print("  update_phase <project_path> <phase> [status]", file=sys.stderr)
        print("  get <project_path>", file=sys.stderr)
        print("  complete <project_path>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    project_path = sys.argv[2]

    try:
        if command == "init":
            if len(sys.argv) < 5:
                print("Error: init requires workflow_type and goal", file=sys.stderr)
                sys.exit(1)
            workflow_type = sys.argv[3]
            goal = sys.argv[4]
            state = init_workflow(project_path, workflow_type, goal)
            print(json.dumps(state, indent=2))

        elif command == "update_phase":
            if len(sys.argv) < 4:
                print("Error: update_phase requires phase_name", file=sys.stderr)
                sys.exit(1)
            phase_name = sys.argv[3]
            status = sys.argv[4] if len(sys.argv) > 4 else "in_progress"
            state = update_phase(project_path, phase_name, status)
            if state:
                print(json.dumps(state, indent=2))
            else:
                sys.exit(1)

        elif command == "get":
            state = get_state(project_path)
            if state:
                print(json.dumps(state, indent=2))
            else:
                print("No workflow found", file=sys.stderr)
                sys.exit(1)

        elif command == "complete":
            state = complete_workflow(project_path)
            if state:
                print(json.dumps(state, indent=2))
            else:
                sys.exit(1)

        else:
            print(f"Error: Unknown command: {command}", file=sys.stderr)
            print("\nValid commands: init, update_phase, get, complete", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

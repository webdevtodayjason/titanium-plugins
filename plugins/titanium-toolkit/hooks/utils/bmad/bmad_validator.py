#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
BMAD Document Validator Utility

Validates BMAD documents match required structure and completeness.

Commands:
    brief <file_path>         Validate product brief
    prd <file_path>           Validate PRD
    architecture <file_path>  Validate architecture
    epic <file_path>          Validate epic
    all <bmad_dir>            Validate all documents in backlog

Examples:
    uv run bmad_validator.py prd bmad-backlog/prd/prd.md
    uv run bmad_validator.py all bmad-backlog/
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List


def validate_brief(file_path: str) -> Dict:
    """
    Validate Product Brief has all required sections.

    Args:
        file_path: Path to product-brief.md

    Returns:
        Validation results dict
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Cannot read file: {e}"],
            "warnings": [],
            "missing_sections": []
        }

    required_sections = [
        "Executive Summary",
        "Problem Statement",
        "Proposed Solution",
        "Target Users",
        "Goals & Success Metrics",
        "MVP Scope",
        "Post-MVP Vision",
        "Technical Considerations",
        "Constraints & Assumptions",
        "Risks & Open Questions",
        "Next Steps"
    ]

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_sections": []
    }

    # Check for required sections
    for section in required_sections:
        if section not in content:
            results["valid"] = False
            results["missing_sections"].append(section)

    # Check for header
    if not re.search(r'#\s+Product Brief:', content):
        results["errors"].append("Missing main header: # Product Brief: {Name}")

    # Check for version info
    if "**Version:**" not in content:
        results["warnings"].append("Missing version field")

    if "**Date:**" not in content:
        results["warnings"].append("Missing date field")

    return results


def validate_prd(file_path: str) -> Dict:
    """
    Validate PRD has all required sections.

    Args:
        file_path: Path to prd.md

    Returns:
        Validation results dict
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Cannot read file: {e}"],
            "warnings": [],
            "missing_sections": []
        }

    required_sections = [
        "Executive Summary",
        "Product Overview",
        "Success Metrics",
        "Feature Requirements",
        "User Stories",
        "Technical Requirements",
        "Data Requirements",
        "AI/ML Requirements",
        "Design Requirements",
        "Go-to-Market Strategy",
        "Risks & Mitigation",
        "Open Questions",
        "Appendix"
    ]

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_sections": []
    }

    # Check for required sections
    for section in required_sections:
        if section not in content:
            results["valid"] = False
            results["missing_sections"].append(section)

    # Check for header
    if not re.search(r'#\s+Product Requirements Document', content):
        results["errors"].append("Missing main header")

    # Check for metadata
    if "**Document Version:**" not in content:
        results["warnings"].append("Missing document version")

    if "**Last Updated:**" not in content:
        results["warnings"].append("Missing last updated date")

    # Check for user stories format
    if "User Stories" in content:
        # Should have "As a" pattern
        if "As a" not in content:
            results["warnings"].append("User stories missing 'As a... I want... so that' format")

    # Check for acceptance criteria
    if "Feature Requirements" in content or "User Stories" in content:
        if "Acceptance Criteria:" not in content and "- [ ]" not in content:
            results["warnings"].append("Missing acceptance criteria checkboxes")

    return results


def validate_architecture(file_path: str) -> Dict:
    """
    Validate Architecture document completeness.

    Args:
        file_path: Path to architecture.md

    Returns:
        Validation results dict
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Cannot read file: {e}"],
            "warnings": [],
            "missing_sections": []
        }

    required_sections = [
        "System Overview",
        "Architecture Principles",
        "High-Level Architecture",
        "Component Details",
        "Data Architecture",
        "Infrastructure",
        "Security Architecture",
        "Deployment Strategy",
        "Monitoring & Observability",
        "Appendix"
    ]

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_sections": []
    }

    # Check for required sections
    for section in required_sections:
        if section not in content:
            results["valid"] = False
            results["missing_sections"].append(section)

    # Check for code examples
    if "```sql" not in content and "```python" not in content and "```typescript" not in content:
        results["warnings"].append("Missing code examples (SQL, Python, or TypeScript)")

    # Check for cost estimates
    if "Cost" not in content:
        results["warnings"].append("Missing cost estimates")

    # Check for technology decisions
    if "Technology Decisions" not in content:
        results["warnings"].append("Missing technology decisions table")

    return results


def validate_epic(file_path: str) -> Dict:
    """
    Validate Epic file structure.

    Args:
        file_path: Path to EPIC-*.md

    Returns:
        Validation results dict
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Cannot read file: {e}"],
            "warnings": [],
            "missing_sections": []
        }

    required_fields = [
        "**Epic Owner:**",
        "**Priority:**",
        "**Status:**",
        "**Estimated Effort:**"
    ]

    required_sections = [
        "Epic Description",
        "Business Value",
        "Success Criteria",
        "User Stories",
        "Dependencies",
        "Definition of Done"
    ]

    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_sections": [],
        "missing_fields": []
    }

    # Check for required fields
    for field in required_fields:
        if field not in content:
            results["valid"] = False
            results["missing_fields"].append(field)

    # Check for required sections
    for section in required_sections:
        if section not in content:
            results["valid"] = False
            results["missing_sections"].append(section)

    # Check for story format
    story_matches = re.findall(r'### STORY-(\d+)-(\d+):', content)
    if not story_matches:
        results["errors"].append("No stories found (expecting STORY-XXX-YY format)")

    # Check stories have acceptance criteria
    if story_matches:
        has_criteria = "Acceptance Criteria:" in content or "**Acceptance Criteria:**" in content
        if not has_criteria:
            results["warnings"].append("Stories missing acceptance criteria")

        # Check for "As a... I want... so that" format
        has_user_story_format = "As a" in content and "I want" in content and "so that" in content
        if not has_user_story_format:
            results["warnings"].append("Stories missing user story format (As a... I want... so that...)")

    return results


def validate_all(bmad_dir: str) -> Dict:
    """
    Validate all documents in BMAD backlog.

    Args:
        bmad_dir: Path to bmad-backlog directory

    Returns:
        Combined validation results
    """
    bmad_path = Path(bmad_dir)

    results = {
        "brief": None,
        "prd": None,
        "architecture": None,
        "epics": [],
        "overall_valid": True
    }

    # Validate brief (optional)
    brief_path = bmad_path / "product-brief.md"
    if brief_path.exists():
        results["brief"] = validate_brief(str(brief_path))
        if not results["brief"]["valid"]:
            results["overall_valid"] = False

    # Validate PRD (required)
    prd_path = bmad_path / "prd" / "prd.md"
    if prd_path.exists():
        results["prd"] = validate_prd(str(prd_path))
        if not results["prd"]["valid"]:
            results["overall_valid"] = False
    else:
        results["overall_valid"] = False
        results["prd"] = {"valid": False, "errors": ["PRD not found"]}

    # Validate architecture (required)
    arch_path = bmad_path / "architecture" / "architecture.md"
    if arch_path.exists():
        results["architecture"] = validate_architecture(str(arch_path))
        if not results["architecture"]["valid"]:
            results["overall_valid"] = False
    else:
        results["overall_valid"] = False
        results["architecture"] = {"valid": False, "errors": ["Architecture not found"]}

    # Validate epics (required)
    epics_dir = bmad_path / "epics"
    if epics_dir.exists():
        epic_files = sorted(epics_dir.glob("EPIC-*.md"))
        for epic_file in epic_files:
            epic_result = validate_epic(str(epic_file))
            epic_result["file"] = epic_file.name
            results["epics"].append(epic_result)
            if not epic_result["valid"]:
                results["overall_valid"] = False
    else:
        results["overall_valid"] = False

    return results


def print_validation_results(results: Dict, document_type: str):
    """Print validation results in readable format."""
    print(f"\n{'='*60}")
    print(f"Validation Results: {document_type}")
    print(f"{'='*60}\n")

    if results["valid"]:
        print("✅ VALID - All required sections present")
    else:
        print("❌ INVALID - Missing required content")

    if results.get("missing_sections"):
        print("\n❌ Missing Required Sections:")
        for section in results["missing_sections"]:
            print(f"  - {section}")

    if results.get("missing_fields"):
        print("\n❌ Missing Required Fields:")
        for field in results["missing_fields"]:
            print(f"  - {field}")

    if results.get("errors"):
        print("\n❌ Errors:")
        for error in results["errors"]:
            print(f"  - {error}")

    if results.get("warnings"):
        print("\n⚠️  Warnings:")
        for warning in results["warnings"]:
            print(f"  - {warning}")

    print()


def main():
    """CLI interface for validation."""

    if len(sys.argv) < 3:
        print("Usage: bmad_validator.py <command> <file_path>", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  brief <file_path>", file=sys.stderr)
        print("  prd <file_path>", file=sys.stderr)
        print("  architecture <file_path>", file=sys.stderr)
        print("  epic <file_path>", file=sys.stderr)
        print("  all <bmad_dir>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    path = sys.argv[2]

    try:
        if command == "brief":
            results = validate_brief(path)
            print_validation_results(results, "Product Brief")
            sys.exit(0 if results["valid"] else 1)

        elif command == "prd":
            results = validate_prd(path)
            print_validation_results(results, "PRD")
            sys.exit(0 if results["valid"] else 1)

        elif command == "architecture":
            results = validate_architecture(path)
            print_validation_results(results, "Architecture")
            sys.exit(0 if results["valid"] else 1)

        elif command == "epic":
            results = validate_epic(path)
            print_validation_results(results, f"Epic ({Path(path).name})")
            sys.exit(0 if results["valid"] else 1)

        elif command == "all":
            results = validate_all(path)

            print(f"\n{'='*60}")
            print(f"Complete Backlog Validation: {path}")
            print(f"{'='*60}\n")

            if results["overall_valid"]:
                print("✅ ALL DOCUMENTS VALID\n")
            else:
                print("❌ VALIDATION FAILED\n")

            # Print individual results
            if results["brief"]:
                print("Product Brief:", "✅ Valid" if results["brief"]["valid"] else "❌ Invalid")
            else:
                print("Product Brief: (not found - optional)")

            if results["prd"]:
                print("PRD:", "✅ Valid" if results["prd"]["valid"] else "❌ Invalid")
            else:
                print("PRD: ❌ Not found (required)")

            if results["architecture"]:
                print("Architecture:", "✅ Valid" if results["architecture"]["valid"] else "❌ Invalid")
            else:
                print("Architecture: ❌ Not found (required)")

            print(f"Epics: {len(results['epics'])} found")
            for epic in results["epics"]:
                status = "✅" if epic["valid"] else "❌"
                print(f"  {status} {epic['file']}")

            print(f"\n{'='*60}\n")

            # Print details if invalid
            if not results["overall_valid"]:
                if results["prd"] and not results["prd"]["valid"]:
                    print_validation_results(results["prd"], "PRD")

                if results["architecture"] and not results["architecture"]["valid"]:
                    print_validation_results(results["architecture"], "Architecture")

                for epic in results["epics"]:
                    if not epic["valid"]:
                        print_validation_results(epic, f"Epic {epic['file']}")

            sys.exit(0 if results["overall_valid"] else 1)

        else:
            print(f"Error: Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

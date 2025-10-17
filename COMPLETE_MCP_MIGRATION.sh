#!/bin/bash

# Complete MCP Migration Script for Titanium Toolkit
# This script updates all remaining bmad-start.md references to use MCP tools

cd "$(dirname "$0")/plugins/titanium-toolkit/commands" || {
    echo "Error: Failed to change directory to plugins/titanium-toolkit/commands" >&2
    exit 1
}

echo "Updating bmad-start.md to use MCP tools..."

# Replace all bmad_generator calls
perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_generator\.py brief "(.*?)" "\$\(pwd\)"|mcp__plugin_titanium-toolkit_tt__bmad_generator(\n  doc_type: "brief",\n  input_path: "$1",\n  project_path: "\$(pwd)"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_generator\.py prd "bmad-backlog/product-brief\.md" "\$\(pwd\)"|mcp__plugin_titanium-toolkit_tt__bmad_generator(\n  doc_type: "prd",\n  input_path: "bmad-backlog/product-brief.md",\n  project_path: "\$(pwd)"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_generator\.py architecture "bmad-backlog/prd/prd\.md" "\$\(pwd\)"|mcp__plugin_titanium-toolkit_tt__bmad_generator(\n  doc_type: "architecture",\n  input_path: "bmad-backlog/prd/prd.md",\n  project_path: "\$(pwd)"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_generator\.py index "bmad-backlog/epics/" "\$\(pwd\)"|mcp__plugin_titanium-toolkit_tt__bmad_generator(\n  doc_type: "index",\n  input_path: "bmad-backlog/epics/",\n  project_path: "\$(pwd)"\n)|g' bmad-start.md

# Replace all bmad_validator calls
perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_validator\.py brief "bmad-backlog/product-brief\.md"|mcp__plugin_titanium-toolkit_tt__bmad_validator(\n  doc_type: "brief",\n  document_path: "bmad-backlog/product-brief.md"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_validator\.py prd "bmad-backlog/prd/prd\.md"|mcp__plugin_titanium-toolkit_tt__bmad_validator(\n  doc_type: "prd",\n  document_path: "bmad-backlog/prd/prd.md"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_validator\.py architecture "bmad-backlog/architecture/architecture\.md"|mcp__plugin_titanium-toolkit_tt__bmad_validator(\n  doc_type: "architecture",\n  document_path: "bmad-backlog/architecture/architecture.md"\n)|g' bmad-start.md

perl -i -pe 's|uv run \${CLAUDE_PLUGIN_ROOT}/hooks/utils/bmad/bmad_validator\.py epic "(.*?)"|mcp__plugin_titanium-toolkit_tt__bmad_validator(\n  doc_type: "epic",\n  document_path: "$1"\n)|g' bmad-start.md

echo "✅ bmad-start.md updated!"
echo ""
echo "Migration complete! All BMAD commands now use MCP tools."

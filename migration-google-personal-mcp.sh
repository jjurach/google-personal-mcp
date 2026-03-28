#!/bin/bash
# Auto-generated migration script - REVIEW BEFORE EXECUTION
# Project: google-personal-mcp

set -e

# Create safety tag before migration
git tag -a -m 'pre-dev_notes-cleanup' pre-dev_notes-cleanup

# Move untracked files to tmp/ for review
mkdir -p tmp
mv dev_notes/specs/2026-01-27_23-53-21_spec-drive-file-operations.md tmp/2026-01-27_23-53-21_spec-drive-file-operations.md.untracked
mv dev_notes/project_plans/2026-01-27_23-53-21_plan-drive-file-operations.md tmp/2026-01-27_23-53-21_plan-drive-file-operations.md.untracked
mv dev_notes/inbox/prompt-02.md tmp/prompt-02.md.untracked
mv dev_notes/inbox/prompt-01.md tmp/prompt-01.md.untracked

# Create planning directory structure
mkdir -p planning/inbox

# Migrate specs → planning/*-prompt.md
git mv dev_notes/specs/2026-01-27_23-53-21_spec-drive-file-operations.md planning/2026-01-27_23-53-21_spec-drive-file-operations-prompt.md

# Migrate project_plans → planning/*-plan.md
git mv dev_notes/project_plans/2026-01-27_23-53-21_plan-drive-file-operations.md planning/2026-01-27_23-53-21_plan-drive-file-operations-plan.md

# Migrate inbox → planning/inbox/
git mv dev_notes/inbox/prompt-01.md planning/inbox/prompt-01.md
git mv dev_notes/inbox/prompt-02.md planning/inbox/prompt-02.md

# Remove empty directories
rmdir dev_notes/specs 2>/dev/null || true
rmdir dev_notes/project_plans 2>/dev/null || true
rmdir dev_notes/inbox 2>/dev/null || true

echo '✓ Migration complete for google-personal-mcp'
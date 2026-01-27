# Agent Development Index

Reference guide for AI agents (Claude Code, etc.) working on this project.

## Table of Contents

1. **[definition-of-done.md](#definition-of-done)** - Mandatory completion criteria
2. **[mcp-development-guide.md](#development)** - Development and debugging reference
3. **[claude-code-workflows.md](#workflows)** - Practical Claude Code examples
4. **[development.md](#architecture)** - Architecture and design patterns
5. **[phase1-implementation.md](#phase1)** - What was implemented in Phase 1
6. **[todo.md](#roadmap)** - Future enhancements (Phase 2+)
7. **[contributing.md](#contributing)** - Code style and contribution guidelines
8. **[troubleshooting.md](#troubleshooting)** - Common issues and solutions
9. **[overview.md](#overview)** - Project overview
10. **[validation-guide.md](#validation)** - Validation and testing guide

---

## <a name="definition-of-done"></a>definition-of-done.md

**Keywords:** completion criteria, pytest, tests, formatting, integration tests, timeout, slack notification, commit

**Purpose:** Mandatory checklist for completing work in Python projects.

**Contents:**
- Running pytest (unit tests)
- Attempting demo applications with `timeout 30`
- Logging failed integration tests with explanations
- Auto-formatting code (black, ruff)
- Committing changes
- Notifying Slack on completion

**When to use:** Before marking any task as "Done". Review before final commit.

**Key mandatory checks:**
- `pytest tests/ -v` must pass
- Run any demo/integration tests with `timeout 30` protection
- Log all test failures with root cause analysis
- Apply black, ruff formatting
- Commit changes

---

## <a name="development"></a>mcp-development-guide.md

**Keywords:** setup, running server, adding tools, debugging techniques, logging, audit logs, component testing, issues, solutions

**Purpose:** Complete reference for developing and debugging the MCP server.

**Contents:**
- Project architecture overview
- Setting up development environment
- Running the server (3 options)
- Adding new tools (3-step process)
- Debugging techniques (5 methods: logging, audit logs, component testing, breakpoints, mocking)
- Common issues and fixes
- Testing workflow
- Code quality checks
- Deployment debugging

**When to use:** Understanding how to develop features, debug issues, or set up the environment.

**Entry points:**
- New to the project? → Read "Part 1: Understanding the MCP Server Architecture"
- Adding a feature? → Read "Part 2: Development Workflow" → "Add a New Tool"
- Something broken? → Read "Part 4: Common Issues & Solutions"

---

## <a name="workflows"></a>claude-code-workflows.md

**Keywords:** Claude Code, workflows, 10 scenarios, exploration commands, development commands, testing, refactoring, security audit, performance

**Purpose:** Practical workflows showing how to use Claude Code for development tasks.

**Contents:**
- 10 real-world development scenarios with step-by-step interactions
- Exploration commands (understanding code)
- Development commands (implementing features)
- Testing commands (verifying changes)
- Workflow tips and best practices
- Example session walkthrough
- When to use Claude Code vs manual development

**When to use:** Learning how to use Claude Code effectively on this project.

**Example scenarios:**
- Debugging a failing test
- Adding a new tool
- Understanding the codebase
- Writing integration tests
- Code quality fixes
- Improving error messages
- Generating documentation
- Performance investigation
- Security audit
- Refactoring boilerplate

---

## <a name="architecture"></a>development.md

**Keywords:** architecture, design patterns, project structure, adding tools, scopes, testing patterns, performance, security, contributing

**Purpose:** In-depth guide to architecture and design patterns used in the project.

**Contents:**
- Architecture overview (layer diagram)
- Project structure with file descriptions
- Design patterns (Service Locator, Context Object, Access Control, Error Handling)
- How to add new tools, scopes, and tests
- Testing patterns (unit, integration, security)
- Performance considerations
- Security considerations (storage, scopes, masking, audit logging)
- Contributing guidelines

**When to use:** Understanding architecture, adding complex features, or implementing new design patterns.

**Key sections:**
- "Key Design Patterns" - How the code is organized
- "Adding New Tools" - 3-step process with full code examples
- "Testing Patterns" - How to write tests with mocks and integration tests

---

## <a name="phase1"></a>phase1-implementation.md

**Keywords:** Phase 1 complete, exceptions, security, logging, testing, documentation, configuration, 44 tests, metrics

**Purpose:** Summary of everything implemented in Phase 1.

**Contents:**
- Executive summary
- All 7 priority areas completed (error handling, security, logging, testing, documentation, standards, configuration)
- Files created (18) and modified (8)
- Test results (44/44 passing)
- Coverage reports
- Key architectural improvements
- Migration guide for existing installations
- Next steps for Phase 2

**When to use:** Understanding what was already implemented and why.

**Key accomplishments:**
- Custom exception hierarchy
- Credential masking
- Request ID propagation
- Structured JSON logging
- Audit logging
- 44 automated tests
- Retry logic with backoff
- .env file support
- Environment-based config

---

## <a name="roadmap"></a>todo.md

**Keywords:** Phase 2, deferred, encryption, plugins, async, caching, pagination, rate limiting, circuit breaker

**Purpose:** Planned future enhancements deferred from Phase 1.

**Contents:**
- Credential encryption at rest (Approach A: OS Keyring, Approach B: File-based)
- Extension & plugin system (tool loader, service extensibility)
- Async MCP execution (async tools, testing strategies)
- Performance optimization (caching, pagination, connection pooling)
- Operational concerns (rate limiting, quota management, graceful degradation)

**When to use:** Planning Phase 2 work or understanding deferred features.

**Deferred because:** Complex to implement, lower priority than Phase 1 infrastructure.

---

## <a name="contributing"></a>contributing.md

**Keywords:** setup, code style, testing, documentation, commit messages, pull requests, issues, code of conduct

**Purpose:** Guidelines for contributing to the project.

**Contents:**
- Development setup (prerequisites, virtual environment, dependencies)
- Code style (ruff, black, mypy, pylint, pre-commit)
- Commit message guidelines
- Testing requirements
- Documentation requirements
- Pull request process
- Issue reporting (bugs and features)
- Code of conduct

**When to use:** Before committing changes or submitting contributions.

**Essential commands:**
- `ruff check src/` - Check for issues
- `black src/` - Format code
- `mypy src/` - Type check
- `pytest tests/ -v` - Run tests

---

## <a name="troubleshooting"></a>troubleshooting.md

**Keywords:** issues, solutions, credentials, tokens, configuration, permissions, startup, import, logging, performance, audit

**Purpose:** Solutions to common problems developers encounter.

**Contents:**
- Authentication issues (credentials not found, token expired, OAuth failed)
- Configuration issues (alias not found, invalid JSON)
- API permission issues (access denied, files not appearing)
- Server startup issues (silent failures, import errors)
- Logging & debugging (verbose logs, debug mode, audit log inspection)
- Performance issues (slow responses, out of memory)
- Known limitations

**When to use:** Troubleshooting when something isn't working.

**Quick lookup:**
- "credentials.json not found" → Search the document
- "Token expired" → See section 2.2
- Server won't start → See section 5

---

## <a name="overview"></a>overview.md

**Keywords:** project, purpose, features, MCP, Google APIs, Sheets, Drive, deployment

**Purpose:** High-level overview of the project.

**Contents:**
- What is this project
- Key features
- Technology stack
- Deployment options
- Quick start

**When to use:** Getting a quick understanding of what the project does.

---

## <a name="validation"></a>validation-guide.md

**Keywords:** validation, testing, coverage, quality, code review, deployment

**Purpose:** Validation and testing guidelines.

**Contents:**
- Test coverage expectations
- Validation checklist
- Code review criteria
- Pre-deployment validation

**When to use:** Validating changes before deployment.

---

## Quick Reference for Agents

### When Starting a Task

1. **Read definition-of-done.md** - Know what "Done" means
2. **Check contributing.md** - Code style and commit message guidelines
3. **Pick the right reference:**
   - Adding feature? → mcp-development-guide.md + development.md
   - Debugging? → mcp-development-guide.md + troubleshooting.md
   - Using Claude Code? → claude-code-workflows.md

### Before Completing a Task

1. **Run tests:** `pytest tests/ -v`
2. **Format code:** `black src/ && ruff check --fix src/`
3. **Check coverage:** `pytest tests/ --cov=src/google_mcp_core --cov-report=term-missing`
4. **Review changes:** Check git diff before commit
5. **Document changes:** Add docstrings and update relevant docs
6. **Follow definition-of-done.md** - Complete all mandatory checks
7. **Commit:** Write clear commit message (see contributing.md)
8. **Notify:** Post to Slack if configured

### Critical Mandatory Details

**These must be repeated and checked every time:**

```bash
# ALWAYS run tests
pytest tests/ -v

# ALWAYS format before committing
black src/ tests/
ruff check --fix src/ tests/

# ALWAYS check coverage
pytest tests/ --cov=src/google_mcp_core

# ALWAYS attempt integration/demo tests with timeout
timeout 30 python -m google_personal_mcp.server --help

# ALWAYS review changes
git diff --cached

# ALWAYS write clear commit message
git commit -m "verb: description

Detailed explanation of changes."
```

### Document Cross-References

- **definition-of-done.md** ← Start here before marking task complete
- **mcp-development-guide.md** → "Adding a New Tool" section
- **claude-code-workflows.md** → "Workflow 2: Adding a New Tool" for example
- **development.md** → "Adding New Tools" with full patterns
- **contributing.md** → Code style and commit format

### Common Agent Tasks

| Task | Primary Doc | Secondary Doc |
|------|-------------|---------------|
| Add new tool | development.md | mcp-development-guide.md |
| Debug issue | troubleshooting.md | mcp-development-guide.md |
| Write tests | development.md (Testing section) | contributing.md |
| Refactor code | development.md | claude-code-workflows.md |
| Improve error messages | mcp-development-guide.md | contributing.md |
| Add feature | development.md | todo.md (for ideas) |
| Improve performance | claude-code-workflows.md (Workflow 8) | development.md |
| Security audit | claude-code-workflows.md (Workflow 9) | development.md |
| Generate documentation | claude-code-workflows.md (Workflow 7) | contributing.md |
| Fix failing test | mcp-development-guide.md (Debugging) | troubleshooting.md |

---

**Last Updated:** 2026-01-27
**Phase 1 Status:** Complete (44/44 tests passing)
**Next Phase:** See todo.md for Phase 2 roadmap

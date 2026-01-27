# Documentation Index

Complete documentation for the Google Personal MCP Server project.

## Quick Start

**For AI Agents:**
- Start with **[AGENTS.md](../AGENTS.md)** - Mandatory workflow and unbreakable rules
- Check **[Definition of Done](definition-of-done.md)** - Quality standards before marking tasks complete

**For Developers:**
- Read **[README.md](../README.md)** - Project overview and setup instructions
- See **[Contributing](contributing.md)** - How to contribute
- Review **[Architecture](architecture.md)** - System design

## For AI Agents

### Core Workflow
- **[AGENTS.md](../AGENTS.md)** - Mandatory A-E workflow (Analyze, Build, Code, Document, Evaluate)
- **[Definition of Done](definition-of-done.md)** - Complete quality checklist for all tasks
- **[Workflows](workflows.md)** - Development workflows for MCP tools and Google API integration
- **[Templates](templates.md)** - Planning document templates and conventions

### Tool-Specific Guides
- **[Claude Code Guide](system-prompts/tools/claude-code.md)** - Complete Claude Code documentation
- **[Aider Guide](system-prompts/tools/aider.md)** - Aider integration
- **[Cline Guide](system-prompts/tools/cline.md)** - Cline integration
- **[Gemini Guide](system-prompts/tools/gemini.md)** - Gemini Code Assist integration

## Architecture & Design

### System Architecture
- **[Architecture](architecture.md)** - Complete system architecture
  - MCP server layer
  - Service layer (SheetsService, DriveService)
  - Authentication layer (OAuth2, profiles)
  - Configuration management
  - CLI tool architecture

- **[Implementation Reference](implementation-reference.md)** - Practical implementation patterns
  - MCP tool development pattern
  - Google API integration pattern
  - Testing patterns (mocking, fixtures)
  - Configuration patterns
  - Error handling patterns
  - CLI command pattern

### Design Documents
- **[Development Guide](development.md)** - Development practices and patterns
- **[Overview](overview.md)** - High-level project overview

## MCP Development

### Guides
- **[MCP Development Guide](mcp-development-guide.md)** - Development and debugging guide
- **[MCP Implementation Guide](mcp-implementation-guide.md)** - Comprehensive implementation guide
- **[Phase 1 Implementation](phase1-implementation.md)** - Initial implementation details
- **[Validation Guide](validation-guide.md)** - Validation strategies

### Examples
- **[MCP Tool Example](examples/mcp-tool-example.md)** - Complete walkthrough of adding a new MCP tool
- **[Google API Integration Example](examples/google-api-integration.md)** - Complete walkthrough of integrating a new Google API
- **[Claude Code Examples](examples/claude-code-examples.md)** - Project-specific Claude Code examples

## Testing & Quality

- **[Definition of Done](definition-of-done.md)** - Quality standards and checklists
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Contributing](contributing.md)** - Code style and contribution guidelines

## System Prompts (Agent Kernel)

The Agent Kernel provides reusable workflows and standards:

- **[Agent Kernel README](system-prompts/README.md)** - Complete Agent Kernel documentation
- **[Universal DoD](system-prompts/principles/definition-of-done.md)** - Universal Definition of Done
- **[Python DoD](system-prompts/languages/python/definition-of-done.md)** - Python-specific standards
- **[Templates](system-prompts/templates/structure.md)** - Document structure templates
- **[Workflows](system-prompts/workflows/README.md)** - Workflow documentation

## Project Management

- **[TODO](todo.md)** - Project tasks and tracking

## Documentation Map

```
docs/
├── README.md                          # This file - documentation index
│
├── For AI Agents
│   ├── definition-of-done.md         # Quality standards (extends Agent Kernel)
│   ├── workflows.md                  # Development workflows
│   ├── templates.md                  # Planning templates
│   └── system-prompts/               # Agent Kernel (universal standards)
│       ├── README.md                 # Agent Kernel overview
│       ├── principles/               # Universal principles
│       ├── languages/python/         # Python-specific standards
│       ├── templates/                # Document templates
│       ├── workflows/                # Workflow guides
│       └── tools/                    # Tool-specific guides
│
├── Architecture & Design
│   ├── architecture.md               # System architecture
│   ├── implementation-reference.md   # Implementation patterns
│   ├── development.md                # Development practices
│   └── overview.md                   # Project overview
│
├── MCP Development
│   ├── mcp-development-guide.md      # Development & debugging
│   ├── mcp-implementation-guide.md   # Comprehensive guide
│   ├── phase1-implementation.md      # Implementation details
│   ├── validation-guide.md           # Validation strategies
│   └── examples/                     # Complete examples
│       ├── mcp-tool-example.md       # MCP tool walkthrough
│       ├── google-api-integration.md # API integration walkthrough
│       └── claude-code-examples.md   # Claude Code examples
│
├── Testing & Quality
│   ├── troubleshooting.md            # Common issues
│   └── contributing.md               # Code style & contribution
│
└── Project Management
    └── todo.md                       # Task tracking
```

## Navigation Tips

### Finding Information

**"How do I add a new MCP tool?"**
→ [MCP Tool Example](examples/mcp-tool-example.md) or [Implementation Reference](implementation-reference.md)

**"How do I integrate a new Google API?"**
→ [Google API Integration Example](examples/google-api-integration.md)

**"What are the quality standards?"**
→ [Definition of Done](definition-of-done.md)

**"What is the system architecture?"**
→ [Architecture](architecture.md)

**"How do I write tests?"**
→ [Implementation Reference - Testing Patterns](implementation-reference.md#testing-patterns)

**"How do I use Claude Code with this project?"**
→ [Claude Code Examples](examples/claude-code-examples.md) or [Claude Code Guide](system-prompts/tools/claude-code.md)

**"What workflows should I follow?"**
→ [Workflows](workflows.md)

**"Where are the document templates?"**
→ [Templates](templates.md) or [Agent Kernel Templates](system-prompts/templates/structure.md)

### For First-Time Contributors

1. Read [README.md](../README.md) - Project overview
2. Review [Architecture](architecture.md) - Understand the system
3. Read [Contributing](contributing.md) - Code standards
4. Check [MCP Tool Example](examples/mcp-tool-example.md) - See practical example
5. Review [Definition of Done](definition-of-done.md) - Quality checklist

### For AI Agents Starting Work

1. Read [AGENTS.md](../AGENTS.md) - Mandatory workflow
2. Check [Definition of Done](definition-of-done.md) - Quality standards
3. Review [Workflows](workflows.md) - Development processes
4. Use [Templates](templates.md) - For planning documents

## See Also

- **[Project README](../README.md)** - Main project documentation
- **[AGENTS.md](../AGENTS.md)** - Agent workflow and rules
- **[CLAUDE.md](../CLAUDE.md)** - Claude Code instructions

---
Last Updated: 2026-01-27

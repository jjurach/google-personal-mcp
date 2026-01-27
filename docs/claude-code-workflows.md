# Claude Code Development Workflows

This guide demonstrates how to use Claude Code (the Claude CLI tool) to develop, debug, and improve the MCP server.

## Part 1: Understanding Claude Code

Claude Code is an interactive CLI that allows you to:
- Ask questions about your codebase
- Read and understand files
- Run commands and tests
- Write and modify code
- Debug issues systematically

### Starting Claude Code

```bash
cd /home/phaedrus/AiSpace/google-personal-mcp
claude-code
```

This drops you into an interactive session where you can ask Claude to explore, develop, and debug your project.

## Part 2: Practical Development Workflows

### Workflow 1: Debugging a Failing Test

**Scenario:** Test fails, you need to find and fix the issue

```
> pytest tests/test_config.py::TestLoadEnvFile::test_load_env_file_basic -v

# Claude runs the test and shows the failure

> read tests/test_config.py

# Claude reads the test file to understand what it's testing

> read src/google_mcp_core/config.py

# Claude reads the implementation

> I see the issue - the function doesn't handle empty files correctly.
> Let me fix it.

# Claude identifies the bug and creates a fix

> run pytest tests/test_config.py::TestLoadEnvFile -v

# Claude verifies all similar tests now pass
```

### Workflow 2: Adding a New Tool

**Scenario:** You want to add "delete_sheet" tool to the MCP server

```
> Add a tool that deletes a sheet from a spreadsheet.
>
> Requirements:
> - Tool name: delete_sheet
> - Parameters: sheet_alias (str), sheet_name (str)
> - Should use SheetsService
> - Should follow the existing error handling pattern
> - Include tests

# Claude workflow:
# 1. Reads sheets.py to understand the structure
# 2. Implements delete_sheet method in SheetsService
# 3. Reads server.py to understand tool pattern
# 4. Registers tool in server.py
# 5. Writes tests in tests/test_sheets_service.py
# 6. Runs pytest to verify everything works
```

**What Claude will do:**
1. Examine existing tools for patterns
2. Implement the method in the service
3. Register the tool with proper error handling
4. Write comprehensive tests
5. Run tests to verify

### Workflow 3: Understanding the Codebase

**Scenario:** You're new to the project and need to understand how it works

```
> Explain how authentication works in this project

# Claude:
# 1. Searches for auth-related files
# 2. Reads auth.py
# 3. Traces how GoogleContext uses credentials
# 4. Explains the full flow with code references
```

**Example follow-ups:**

```
> What happens when a tool is called?

# Claude traces:
# - Tool invocation in server.py
# - Error handling pattern
# - Request ID tracking
# - Audit logging
```

```
> Show me all the places where credentials could leak

# Claude:
# 1. Greps for credential patterns
# 2. Reviews each location
# 3. Identifies potential issues
# 4. Suggests fixes
```

### Workflow 4: Writing Integration Tests

**Scenario:** Need comprehensive tests for the config system

```
> Create an integration test that:
> 1. Creates a ConfigManager with temporary files
> 2. Tests .env file loading
> 3. Tests environment-based config loading
> 4. Verifies all sheets are accessible
>
> Use pytest fixtures and tmp_path for temporary files.

# Claude:
# 1. Reviews conftest.py for available fixtures
# 2. Reads test_config.py for patterns
# 3. Creates test class with multiple test methods
# 4. Uses tmp_path for temporary files
# 5. Writes clear assertions
# 6. Runs tests to verify they work
```

### Workflow 5: Code Quality Fixes

**Scenario:** You want to ensure code quality across the project

```
> Run code quality checks on all source files

# Claude:
# 1. Runs: ruff check src/
# 2. Runs: black --check src/
# 3. Runs: mypy src/
# 4. Reports all issues found

> Now fix all the issues

# Claude:
# 1. Runs: black src/ tests/ (auto-formats)
# 2. Runs: ruff check --fix src/ (auto-fixes)
# 3. Identifies remaining issues for manual fixing
# 4. Fixes type hint issues
# 5. Re-runs all checks to verify
```

### Workflow 6: Improving Error Messages

**Scenario:** Error messages are too generic, need to be more helpful

```
> Improve error messages in auth.py
>
> Current issues:
> - "Authentication failed" doesn't tell users why
> - No helpful instructions for fixing
>
> Make each error specific with actionable advice

# Claude:
# 1. Reads auth.py
# 2. Identifies error scenarios:
#    - credentials.json not found
#    - token expired
#    - scopes insufficient
#    - OAuth flow interrupted
# 3. Updates each error message with:
#    - Clear description of what happened
#    - Why it happened
#    - How to fix it
# 4. Tests error paths to verify messages work
```

### Workflow 7: Documentation Generation

**Scenario:** Need API documentation for a service

```
> Generate API documentation for the SheetsService class
>
> Include:
> - Method signatures with types
> - Docstrings for each method
> - Parameter descriptions
> - Return value descriptions
> - Usage examples

# Claude:
# 1. Reads sheets.py
# 2. Extracts all public methods
# 3. Analyzes parameters and return types
# 4. Generates markdown documentation
# 5. Adds usage examples
# 6. Saves to docs/api/sheets.md
```

### Workflow 8: Performance Investigation

**Scenario:** The list_sheets tool is slow

```
> The list_sheets tool is slow. Help me find the bottleneck.
>
> I suspect multiple API calls are being made.

# Claude:
# 1. Reads server.py list_sheets implementation
# 2. Traces through the call chain
# 3. Identifies:
#    - ConfigManager lookups
#    - GoogleContext initialization
#    - Number of API calls
# 4. Profiles the code
# 5. Suggests optimizations:
#    - Cache service instances
#    - Batch API calls
#    - Reduce redundant calls
# 6. Implements improvements
# 7. Benchmarks before/after
```

### Workflow 9: Security Audit

**Scenario:** Need to audit the code for security issues

```
> Audit the codebase for security issues
>
> Check for:
> - Credential leaks (credentials in logs, errors)
> - Unsafe file operations
> - Insecure API usage
> - Missing input validation
> - Path traversal vulnerabilities

# Claude:
# 1. Searches for suspicious patterns
# 2. Reviews credential handling
# 3. Checks file operations
# 4. Analyzes API calls
# 5. Tests input validation
# 6. Generates report with:
#    - Issues found
#    - Severity level
#    - Recommended fixes
# 7. Implements fixes
```

### Workflow 10: Refactoring Boilerplate

**Scenario:** Too much repeated error handling code

```
> All tools have similar error handling patterns:
>   try:
>       result = do_work()
>       audit_logger.log(success=True)
>       return {"status": "success", ...}
>   except Exception:
>       audit_logger.log(success=False)
>       return {"status": "error", ...}
>
> Create a decorator to eliminate this boilerplate
> and refactor all tools to use it.

# Claude:
# 1. Creates @mcp_tool decorator
# 2. Handles:
#    - Request ID setup/cleanup
#    - Error handling
#    - Audit logging
#    - Credential masking
# 3. Refactors all tools
# 4. Tests to verify nothing breaks
# 5. Result: 50% less error handling code
```

## Part 3: Exploration Commands

### Learn What's in the Codebase

```
# Understand the architecture
> Explain the overall architecture of the MCP server

# Learn about specific components
> What does the GoogleContext class do?
> How does the retry decorator work?
> Where is authentication handled?

# Understand flows
> Show me the authentication flow
> How does a tool invocation work?
> Trace the request ID through the code

# Find things
> Where are API errors handled?
> What files implement the Sheets API?
> Show all places where credentials are used
```

### Search and Analyze

```
# Find patterns
> Find all uses of @mcp.tool() and list the tool names

# Look for issues
> Find all TODO or FIXME comments in the code

# Understand relationships
> Show me all functions that call GoogleContext

# Get metrics
> How many lines of code in each module?
> What's the test coverage for sheets.py?
```

## Part 4: Development Commands

### Building Features

```
# Feature requests
> Add support for reading Google Docs (not just Sheets)
> Implement caching to reduce API calls
> Add rate limiting detection
> Support batch operations

# For each, Claude will:
# 1. Understand the existing pattern
# 2. Design the new feature
# 3. Implement the code
# 4. Write tests
# 5. Verify it works
```

### Fixing Issues

```
# Bug fixes
> Fix the failing test_mask_bearer_token test
> The server doesn't start when config is missing
> API calls fail sometimes - add retry logic
> Errors don't have helpful messages

# For each, Claude will:
# 1. Understand the issue
# 2. Identify the root cause
# 3. Implement a fix
# 4. Write tests
# 5. Verify the fix works
```

### Improving Quality

```
# Code quality
> Refactor this code to be more DRY
> Add better error messages
> Optimize for performance
> Improve test coverage

# Documentation
> Generate API documentation
> Create architecture diagram
> Write developer guide
> Document common issues
```

## Part 5: Testing Commands

```
# Run tests
> Run all tests
> Run tests/test_config.py
> Run tests matching pattern "test_mask"

# Debug tests
> Why is test_load_env_file_basic failing?
> Debug the test_config.py::TestConfigManager tests
> Add more test cases for edge cases

# Coverage
> Show test coverage for sheets.py
> What lines in auth.py aren't covered by tests?
> Improve coverage for config.py
```

## Part 6: Workflow Tips

### 1. Be Specific with Requirements

Bad: "Fix the error"
Good: "The test_load_env_file_basic test fails with KeyError on line 42. Debug and fix."

### 2. Provide Context

```
> I want to add caching for API calls.
>
> Background:
> - We make the same API calls repeatedly
> - Each call takes 500ms
> - We need <100ms response time
> - Current design fetches on every tool invocation
>
> Where should the cache go? Show me the approach.
```

### 3. Request Multi-Step Work

```
> First, show me the current error handling pattern.
> Then, create a decorator that implements it.
> Finally, refactor two example tools to use it.
> Then run all tests to verify.
```

### 4. Ask for Verification

```
> Implement the feature, then:
> 1. Write comprehensive tests
> 2. Run pytest with coverage
> 3. Run code quality checks
> 4. Verify no regressions
```

### 5. Request Documentation

```
> Implement the feature, then document it by:
> 1. Adding docstrings
> 2. Creating usage examples
> 3. Adding to development.md
```

## Part 7: Common Project Commands

### For This MCP Server Project

```
# Understand the project
> What was Phase 1 implementation?
> Explain the authentication flow
> Show the tool registration pattern
> How does audit logging work?

# Develop features
> Add a tool to export sheets to CSV
> Add support for Drive folders
> Implement rate limiting
> Add batch operations

# Fix issues
> Debug authentication failures
> Fix credential leaks
> Improve error messages
> Optimize slow API calls

# Improve quality
> Run all code quality checks
> Improve test coverage
> Add type hints
> Refactor to be DRY

# Documentation
> Generate API documentation
> Create architecture diagram
> Document the request flow
> Write a getting started guide
```

## Part 8: Example Session

Here's what a real Claude Code session might look like:

```bash
$ claude-code
Claude Code v0.x.x

Starting new session in /home/phaedrus/AiSpace/google-personal-mcp

> How does authentication work?

Claude:
[Reads auth.py, context.py, explains flow with code references]

The authentication flow:
1. GoogleContext initializes AuthManager
2. AuthManager loads credentials from file or env var
3. Token is automatically refreshed when expired
4. Services use the context to get authenticated API clients

Code references:
- src/google_mcp_core/auth.py:60-80
- src/google_mcp_core/context.py:15-30

> Show me the tool registration pattern

Claude:
[Reads server.py, explains pattern]

Each tool follows this pattern:
1. Use @mcp.tool() decorator
2. Request ID setup/cleanup
3. Try/catch with specific exceptions
4. Audit logging on success/failure
5. Return structured dict with status

Example in server.py:47-75

> I want to add a delete_sheet tool. Show me what I need to do.

Claude:
[Analyzes patterns, creates implementation plan]

You need to:
1. Add method to SheetsService class (sheets.py)
2. Register @mcp.tool in server.py
3. Write tests in tests/test_sheets_service.py
4. Run pytest to verify

Let me implement this for you...

[Creates the implementation]

Now let me run the tests...

> run pytest tests/test_sheets_service.py -v

[Tests pass]

Done! The delete_sheet tool is ready.

> Add it to the documentation

Claude:
[Updates docs with new tool]

Updated development.md and added to docs/api/sheets.md

> Show me the coverage

Claude:
> run pytest tests/ --cov=src/google_mcp_core --cov-report=term-missing

[Shows coverage report]

Coverage is now 85% overall, 95% for new code.
```

## Part 9: When to Use Claude Code vs Manual Development

### Use Claude Code When:

- You're debugging a complex issue
- You need to understand unfamiliar code
- You're adding a feature and need patterns
- You want to refactor safely
- You need documentation generated
- You're searching for specific patterns

### Manual Development When:

- Simple one-line fixes
- You know exactly what to do
- The task is very specific and small
- You need full control and understanding

For most tasks, Claude Code accelerates development by handling exploration, analysis, and boilerplate, while you focus on decisions and review.

---

This guide gives you practical workflows for using Claude Code effectively on this MCP server project.

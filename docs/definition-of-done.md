# Definition of Done - Google Personal MCP Server

**Referenced from:** [AGENTS.md](../AGENTS.md)

This document defines the "Done" criteria for the Google Personal MCP Server project. It extends the universal Agent Kernel Definition of Done with project-specific requirements.

## Agent Kernel Definition of Done

This project follows the Agent Kernel Definition of Done. **You MUST review these documents first:**

### Universal Requirements

See **[Universal Definition of Done](system-prompts/principles/definition-of-done.md)** for:
- Plan vs Reality Protocol
- Verification as Data
- Codebase State Integrity
- Agent Handoff
- Status tracking in project plans
- dev_notes/ change documentation requirements

### Python Requirements

See **[Python Definition of Done](system-prompts/languages/python/definition-of-done.md)** for:
- Python environment & dependencies
- pytest testing requirements
- Code quality standards (PEP 8, type hints, docstrings)
- File organization
- Coverage requirements (60% minimum)

## Project-Specific Extensions

The following requirements are specific to the Google Personal MCP Server and extend the Agent Kernel DoD:

### 1. MCP Tool Development Requirements

All MCP tools must follow the standard template (see [Implementation Reference](implementation-reference.md)):

**Mandatory Checks:**
- [ ] Tool follows standard template pattern
- [ ] Request ID management: `set_request_id()` at start, `clear_request_id()` in finally block
- [ ] Structured response format: `{"status": "success|error", "result"/"message": ..., "request_id": ...}`
- [ ] Exception handling: All exceptions caught, never raised to MCP layer
- [ ] Credential masking: All errors pass through `mask_credentials()` when not in debug mode
- [ ] Audit logging: Tool calls logged with `audit_logger.log_tool_call()`
- [ ] Service locator used: `get_sheets_service()` or `get_drive_service()` for service instances
- [ ] Docstring includes Args and Returns sections
- [ ] Tool registered with `@mcp.tool()` decorator

**Example verification:**
```bash
# Check tool follows template
grep -A 30 "@mcp.tool()" src/google_personal_mcp/server.py | grep "set_request_id"
grep -A 30 "@mcp.tool()" src/google_personal_mcp/server.py | grep "audit_logger"

# Verify credential masking works
python -c "from google_mcp_core.utils.sanitizer import mask_credentials; assert 'REDACTED' in mask_credentials('Token: ya29.abc123')"
```

### 2. Google API Integration Requirements

When adding support for new Google APIs:

**Mandatory Checks:**
- [ ] OAuth scopes updated in `src/google_mcp_core/auth.py` `SCOPES` constant
- [ ] Service class created following `GoogleContext` pattern
- [ ] Service class uses `context.get_service(name, version)` for API access
- [ ] Service locator function added (e.g., `get_gmail_service()`)
- [ ] API version explicitly specified (no "latest")
- [ ] Service class has no credential management code (delegated to `GoogleContext`)
- [ ] Retry logic applied with `@retry_on_rate_limit` decorator for API calls
- [ ] Access control implemented if needed (e.g., Drive folder restrictions)
- [ ] README.md updated with new OAuth scope and re-authentication instructions

**Example verification:**
```bash
# Check scopes updated
grep "SCOPES = \[" src/google_mcp_core/auth.py

# Check service follows pattern
python -c "from google_mcp_core.sheets import SheetsService; from google_mcp_core.context import GoogleContext; ctx = GoogleContext(); svc = SheetsService(ctx); print('OK')"
```

### 3. Testing Requirements for Google APIs

**Mandatory Checks:**
- [ ] Unit tests use mocked Google APIs via `mock_google_context` fixture
- [ ] NO real API calls in unit tests
- [ ] Integration tests marked with `@pytest.mark.integration`
- [ ] Integration tests skip if credentials unavailable: `@pytest.mark.skipif(not has_credentials(), ...)`
- [ ] Google API responses mocked realistically in unit tests
- [ ] Mock fixtures configured in `tests/conftest.py`
- [ ] Tests clean up temporary resources (files, sheets) after execution

**Unit test pattern:**
```python
def test_operation(mock_sheets_service):
    """Unit test with mocked Google API."""
    # Setup mock response
    mock_sheets_service.service.spreadsheets().get().execute.return_value = {...}

    # Test service method
    result = mock_sheets_service.operation()

    # Verify (no real API calls)
    assert result is not None
```

**Integration test pattern:**
```python
@pytest.mark.integration
@pytest.mark.skipif(not has_credentials(), reason="Requires credentials")
def test_operation_integration():
    """Integration test with real Google API."""
    service = SheetsService(GoogleContext())
    result = service.operation(TEST_RESOURCE_ID)
    assert result is not None
```

**Run tests:**
```bash
# Unit tests only (fast, no credentials needed)
pytest tests/unit/ -v

# Integration tests (requires credentials)
pytest tests/integration/ -v -m integration
```

### 4. Configuration Management Requirements

**Mandatory Checks:**
- [ ] Resource aliases use configuration system (no hardcoded IDs in tools)
- [ ] New resource types added to `AppConfig` model in `config.py`
- [ ] Configuration example updated if new fields added
- [ ] NO real credentials in any committed files
- [ ] NO hardcoded spreadsheet/folder IDs in source code
- [ ] Configuration validation via Pydantic models
- [ ] Profile associations configured correctly for resources

**Pre-commit check:**
```bash
# Check for accidental credential leaks
git diff | grep -E "(credentials|token|api_key|client_secret)" && echo "⚠️  WARNING: Possible credentials in commit"

# Verify no hardcoded IDs
git diff src/ | grep -E '"1[A-Za-z0-9_-]{43}"' && echo "⚠️  WARNING: Possible hardcoded Google resource ID"
```

### 5. CLI Command Requirements

When adding CLI commands:

**Mandatory Checks:**
- [ ] Command handler added to `src/google_mcp_core/cli.py`
- [ ] Command registered in `COMMANDS` dictionary
- [ ] Command reuses service layer (no duplicate logic)
- [ ] Help text provided for command and arguments
- [ ] Error handling: Use `sys.stderr` for errors, exit code 1 on failure
- [ ] Output format user-friendly (not JSON dump)
- [ ] Command tested manually: `google-personal-mcp <group> <command> --help`

**Example verification:**
```bash
# Check command registered
google-personal-mcp --help | grep "new-command"

# Test command execution
google-personal-mcp sheets new-command test-alias
```

### 6. Security & Credential Masking Requirements

**Mandatory Checks:**
- [ ] All tool errors pass through `mask_credentials()` function
- [ ] No credentials in log files (check `~/.config/google-personal-mcp/audit.log`)
- [ ] No credentials in error responses
- [ ] Credential patterns masked: OAuth tokens, API keys, Bearer tokens, file paths
- [ ] Debug mode documented (env var to disable masking): `GOOGLE_PERSONAL_MCP_DEBUG=1`
- [ ] Tests verify masking works: `test_credential_masking()`

**Test masking:**
```bash
# Verify masking works
python -c "
from google_mcp_core.utils.sanitizer import mask_credentials
test_cases = [
    'Token: ya29.abc123',
    'API key: AIzaSyD...',
    'Bearer: 1//0abc...'
]
for case in test_cases:
    masked = mask_credentials(case)
    assert 'REDACTED' in masked, f'Failed: {case}'
print('✅ All masking tests passed')
"
```

### 7. Integration Test Timeouts

Integration tests may legitimately fail or timeout in certain environments:

**Non-blocking failures:**
- Missing credentials files (`credentials.json` not found)
- Missing Google API access (not authenticated)
- Timeout due to slow imports (first run with Google API client)
- External service unavailable

**These failures don't block commits** but should be investigated for:
- Performance regressions
- New heavy dependencies
- Unexpected API calls on startup

**Example timeout check:**
```bash
# Integration tests should complete within reasonable time
timeout 30 python -m google_personal_mcp.server --help
# Exit code 124 = timeout (investigate but don't block)
# Exit code 0 = success
# Other codes = real errors (investigate)
```

### 8. Documentation Requirements

**Mandatory for MCP tools:**
- [ ] Tool added to README.md tool list
- [ ] Tool parameters documented in docstring
- [ ] Tool return format documented in docstring
- [ ] Architecture.md updated if new service added
- [ ] Implementation-reference.md updated if new pattern introduced
- [ ] OAuth scope changes documented in README

**Mandatory for Google API integration:**
- [ ] New service documented in architecture.md
- [ ] Service class patterns documented in implementation-reference.md
- [ ] Integration examples added to implementation-reference.md
- [ ] OAuth scope requirements documented in README

## Pre-Commit Checklist

Before committing, verify:

**Code Quality:**
- [ ] Black formatting applied: `black src/ tests/`
- [ ] Ruff checks pass: `ruff check src/ tests/`
- [ ] Type hints present for new functions
- [ ] Docstrings present for new functions

**Testing:**
- [ ] All unit tests pass: `pytest tests/unit/ -v`
- [ ] Integration tests pass (or documented why skipped): `pytest tests/integration/ -v -m integration`
- [ ] No real API calls in unit tests
- [ ] Coverage ≥ 60%: `pytest tests/ --cov=src/google_mcp_core`

**Security:**
- [ ] No credentials in code: `git diff | grep -E "(credentials|token|api_key)"`
- [ ] Credential masking works for new error paths
- [ ] No hardcoded resource IDs in code

**MCP Tools:**
- [ ] Tool follows standard template pattern
- [ ] Request ID management implemented
- [ ] Audit logging integrated
- [ ] Structured error responses

**Configuration:**
- [ ] Configuration example updated if needed
- [ ] Resource aliases used (no hardcoded IDs)
- [ ] Profile associations correct

**Documentation:**
- [ ] README updated for new features/tools
- [ ] Architecture docs updated for new services
- [ ] Implementation reference updated for new patterns
- [ ] OAuth scope changes documented

**Commit:**
- [ ] Commit message follows format: `type: description`
- [ ] Co-Authored-By trailer included
- [ ] Changes reviewed with `git diff`
- [ ] Human approval received (for interactive workflows)

## Success Criteria Examples

### Example 1: Adding a New MCP Tool

```bash
# 1. Code formatting
black src/ tests/
ruff check --fix src/ tests/

# 2. Run unit tests
pytest tests/unit/ -v
# Expected: All tests pass, new tool tests included

# 3. Verify tool follows template
grep -A 40 "def new_tool" src/google_personal_mcp/server.py | grep "set_request_id"
grep -A 40 "def new_tool" src/google_personal_mcp/server.py | grep "audit_logger"
grep -A 40 "def new_tool" src/google_personal_mcp/server.py | grep "clear_request_id"

# 4. Check credential masking
python -c "from google_mcp_core.utils.sanitizer import mask_credentials; print(mask_credentials('Error: Token ya29.abc'))"
# Expected: ***REDACTED:OAUTH_TOKEN***

# 5. Verify documentation
grep "new_tool" README.md
# Expected: Tool listed in README

# 6. Commit
git add -A
git commit -m "feat: add new_tool MCP tool

Implements new_tool to handle X operation.

- Service layer method added
- MCP tool follows standard template
- Unit tests added (all passing)
- Documentation updated

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Example 2: Adding Google API Integration

```bash
# 1. Verify scopes updated
grep "gmail.readonly" src/google_mcp_core/auth.py
# Expected: Found in SCOPES list

# 2. Run tests
pytest tests/ -v

# 3. Verify service follows pattern
python -c "from google_mcp_core.gmail import GmailService; from google_mcp_core.context import GoogleContext; ctx = GoogleContext(); svc = GmailService(ctx); print('✅ Service initialized')"

# 4. Check documentation
grep "Gmail" README.md
grep "GmailService" docs/architecture.md

# 5. User re-authentication note
grep "rm.*token.json" README.md
# Expected: Instructions to delete token.json for re-auth

# 6. Commit
git add -A
git commit -m "feat: add Gmail API integration

Adds support for Gmail API v1.

- OAuth scope added: gmail.readonly
- GmailService created following GoogleContext pattern
- list_messages() and get_message() methods
- Unit tests with mocked API
- Documentation updated

Users must re-authenticate: rm ~/.config/google-personal-mcp/profiles/*/token.json

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

## Common Pitfalls

**DON'T:**
- ❌ Make real Google API calls in unit tests
- ❌ Hardcode spreadsheet IDs or folder IDs in code
- ❌ Commit files with real credentials
- ❌ Skip credential masking for "simple" errors
- ❌ Raise exceptions in MCP tools (return error responses instead)
- ❌ Skip audit logging for tool calls
- ❌ Use `print()` for errors (use logging or structured errors)
- ❌ Skip request ID management

**DO:**
- ✅ Mock all Google APIs in unit tests
- ✅ Use resource aliases from configuration
- ✅ Mask ALL credentials in errors and logs
- ✅ Return structured error responses from MCP tools
- ✅ Log all tool calls to audit trail
- ✅ Use `set_request_id()` and `clear_request_id()`
- ✅ Follow standard tool template pattern
- ✅ Document OAuth scope changes with re-auth instructions

## See Also

- [AGENTS.md](../AGENTS.md) - Core A-E workflow
- [Universal DoD](system-prompts/principles/definition-of-done.md) - Agent Kernel universal requirements
- [Python DoD](system-prompts/languages/python/definition-of-done.md) - Agent Kernel Python requirements
- [Architecture](architecture.md) - System design
- [Implementation Reference](implementation-reference.md) - Code patterns and templates
- [Workflows](workflows.md) - Development workflows

---
Last Updated: 2026-01-27

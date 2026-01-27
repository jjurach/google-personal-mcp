# Definition of Done - Python Projects

**Referenced from:** [AGENTS.md](./AGENTS.md)

Mandatory checklist for completing work on Python projects. All items must be completed before marking a task as "Done" and committing changes.

---

## Pre-Work: Human Review & Approval

Before starting any of these checks, pause for human review if this is an interactive workflow:

1. **Present changes for review**
   - Show git diff of all changes
   - Highlight breaking changes (if any)
   - Note any external dependencies added
   - Request explicit approval: "Ready to proceed with formatting, testing, and commit?"

2. **Only proceed if:**
   - Human says "yes" or "approved"
   - OR workflow is fully autonomous (CI/CD)

---

## Phase 1: Automatic Formatting

Apply automatic code formatting to ensure consistency:

```bash
# Format code
black src/ tests/

# Auto-fix common issues
ruff check --fix src/ tests/
```

**What happens if it fails:**
- Check for syntax errors in modified files
- Verify Python version compatibility (3.8+)
- Review file permissions
- Log error and stop (don't proceed to tests)

**Log example:**
```
❌ Formatting failed: black returned exit code 1
   File: src/google_mcp_core/config.py:42
   Issue: Syntax error in function definition
   Fix: Review syntax and try again
```

---

## Phase 2: Unit Tests

Run all unit tests with verbose output:

```bash
pytest tests/ -v
```

**Success criteria:**
- All tests pass (100% pass rate)
- No skipped tests in critical paths
- Coverage meets minimum (60%)

**What happens if tests fail:**

1. **Run with detailed output:**
   ```bash
   pytest tests/ -v --tb=short
   ```

2. **For each failed test, log:**
   ```
   ❌ FAILED: tests/test_config.py::TestLoadEnvFile::test_load_env_file_basic

   Error: KeyError: 'TEST_VAR'

   Explanation: The test expects the env var to be set, but it wasn't loaded by load_env_file()

   Root cause: load_env_file() doesn't handle .env files in current directory

   Fix for next iteration:
   - Check if .env exists in cwd before looking in home directory
   - Or ensure test sets up env var before calling function
   - Or mock the load_env_file() function in tests
   ```

3. **Do NOT proceed** to integration tests until unit tests pass

**Example test run:**
```bash
$ pytest tests/ -v
collected 44 items

tests/test_config.py::TestLoadEnvFile::test_load_env_file_basic PASSED   [  2%]
tests/test_config.py::TestLoadEnvFile::test_load_env_file_with_comments PASSED [  4%]
...
====== 44 passed in 0.32s ======

✅ Unit tests PASSED (44/44)
```

---

## Phase 3: Integration & Demo Tests

Attempt to run any demo applications or integration tests described in the codebase:

```bash
# Timeout protection: 30 seconds maximum per test
timeout 30 python -m google_personal_mcp.server --help
timeout 30 python -c "from google_mcp_core.config import ConfigManager; ConfigManager()"
```

**When tests pass:**
```
✅ Integration tests PASSED
   - Server help printed successfully
   - ConfigManager initialized without errors
```

**When tests fail or timeout:**

Log each failure with this format:

```
⚠️  INTEGRATION TEST FAILED/TIMEOUT
   Test: timeout 30 python -m google_personal_mcp.server --help

   Exit code: 124 (timeout) OR [other error code]

   Last output:
   [print last 20 lines of output here]

   Explanation: The server took longer than 30 seconds to initialize
   OR: Missing required environment variables
   OR: Configuration file not found

   Root cause: [Best guess of why this failed]
   - Could be slow imports (google-api-client takes time)
   - Could be attempting real API connection
   - Could be missing credentials file
   - Could be syntax error that wasn't caught by unit tests

   Fix for next iteration:
   - Mock Google API client to speed up imports
   - Skip real API calls in test mode
   - Verify credentials files exist before attempting
   - Check for syntax errors in modified files

   Status: ⚠️  NON-BLOCKING (integration tests may legitimately fail with credentials missing)
           But should investigate for performance regressions or new dependencies
```

**Non-blocking failures:**

These failures don't block commit if they're environmental:
- Missing credentials files (`credentials.json` not found)
- Missing Google API access (legitimate when not authenticated)
- Timeout due to slow imports (expected for first run)
- External service unavailable

**Blocking failures:**

These DO block commit:
- Syntax errors
- Import errors (missing modules)
- Code crashes (unhandled exceptions)
- Configuration parsing errors

---

## Phase 4: Code Quality Checks

Run type checking and linting:

```bash
# Type checking
mypy src/ --ignore-missing-imports

# Additional linting (optional, but recommended)
pylint src/ --disable=all --enable=E,F
```

**What happens if checks fail:**

Log warnings (non-blocking):

```
⚠️  CODE QUALITY ISSUES FOUND
   Type checking: 3 untyped variables
   Linting: 2 unused imports

   Note: These are warnings, not blocking
   Recommendation: Fix in next iteration

   Examples:
   - src/google_mcp_core/config.py:42: error: Untyped variable 'config'
   - src/google_mcp_core/utils/sanitizer.py:15: unused 'import os'
```

---

## Phase 5: Coverage Report

Check test coverage:

```bash
pytest tests/ --cov=src/google_mcp_core --cov-report=term-missing
```

**What to look for:**

```
Coverage report:
  src/google_mcp_core/config.py: 85% coverage (missing lines: 36-37, 53-54)
  src/google_mcp_core/exceptions.py: 100% coverage

✅ Coverage is above minimum (60%)

Note: New files should have >80% coverage if possible
```

**Log if coverage decreased:**

```
⚠️  COVERAGE DECREASED
   Before: 75%
   After: 70%
   Change: -5%

   Files with new uncovered code:
   - src/google_mcp_core/config.py: 4 new lines uncovered

   Recommendation: Add tests for new code paths
```

---

## Phase 6: Review Changes

Before committing, review all changes:

```bash
git diff --cached
git status
```

**What to check:**

1. **No accidental changes:**
   - No .env files with real credentials
   - No personal config files
   - No node_modules, __pycache__, .venv
   - All changes are intentional

2. **File changes make sense:**
   - Files that should be modified are modified
   - Files that shouldn't be changed aren't changed
   - No merge conflicts or git artifacts

3. **Examples of what to verify:**
   ```
   # Good: Intentional changes
   +       import pdb; pdb.set_trace()  # Debug
   -       return None
   +       return result

   # Bad: Accidental changes
   +       "api_key": "sk_live_abc123..."  # Real credential!
   +       os.chmod(filename, 0o777)  # Insecure permissions

   # Bad: Unnecessary changes
   +       # TODO: Fix this someday
   +       import unused_module
   ```

4. **Log any concerns:**
   ```
   ⚠️  REVIEW ISSUE FOUND
      File: src/google_mcp_core/config.py
      Change: Added import of 'unused_module'
      Issue: This import is never used in the file
      Action: Remove the import
   ```

---

## Phase 7: Commit Changes

Write a clear, atomic commit message:

```bash
git commit -m "verb: description

Detailed explanation of what changed and why.

- Bullet 1
- Bullet 2"
```

**Commit message format (from contributing.md):**

```
Start with a verb: Add, Fix, Update, Refactor, etc.
First line: 50 characters or less
Blank line
Body: Explain what and why (not how)
Reference issue numbers if applicable

Example:
  Add credential masking utility for logs

  Implemented mask_credentials() function to prevent
  credential leakage in error messages and logs.

  - Masks Bearer tokens with ***REDACTED***
  - Masks OAuth tokens (ya29...) with specific marker
  - Masks API keys and file IDs
  - Disabled in debug mode for troubleshooting

  Fixes #123
```

**Log the commit:**

```
✅ COMMIT CREATED
   Hash: a1b2c3d
   Message: "Add credential masking utility for logs"
   Files changed: 3
   Insertions: +87
   Deletions: -12
```

---

## Phase 8: Slack Notification (If Configured)

Notify team of completed work (if Slack webhook is configured):

```
📦 Task Completed: Add credential masking utility

Status: ✅ SUCCESS

Changes:
- src/google_mcp_core/utils/sanitizer.py (new)
- tests/test_sanitizer.py (new, 15 tests passing)
- src/google_personal_mcp/server.py (updated)

Tests:
- 44/44 unit tests passing ✅
- Integration tests: OK (non-blocking)
- Coverage: 85% (target 60%) ✅

Quality:
- Code formatted (black, ruff)
- Type checked (mypy)
- No new warnings

Commit: a1b2c3d - Add credential masking utility for logs

Ready for review and merge.
```

---

## Summary Checklist

Before saying "Done", verify all of these:

- [ ] **Human approved changes** (if interactive workflow)
- [ ] **Code formatted** with `black` and `ruff --fix`
- [ ] **Unit tests pass** with `pytest tests/ -v` (44/44 ✅)
- [ ] **Integration tests attempted** with `timeout 30` protection
- [ ] **Failed integration tests logged** with root cause analysis
- [ ] **Code quality checked** with `mypy` (warnings logged)
- [ ] **Coverage reviewed** (must be ≥60%, ideally ≥80%)
- [ ] **Changes reviewed** with `git diff --cached`
- [ ] **Commit message written** following format in contributing.md
- [ ] **Changes committed** with `git commit -m "..."`
- [ ] **Slack notified** with summary (if configured)
- [ ] **No real credentials in commit**
- [ ] **No large files in commit** (>1MB)
- [ ] **No test files skipped** (unless explicitly deferred)

---

## When Tests Fail

**Mandatory steps:**

1. **Don't ignore failures** - Every failure must be understood

2. **Log the failure:**
   ```
   ❌ TEST FAILURE LOGGED

   Test: tests/test_config.py::TestLoadEnvFile::test_load_env_file_basic
   Error: KeyError: 'TEST_VAR'

   Explanation: Environment variable not set by load_env_file()

   Root cause: File not found in expected locations
              OR File has no TEST_VAR line
              OR File permissions prevent reading

   Fix for next iteration:
   - Debug load_env_file() with verbose output
   - Check file exists at expected path
   - Verify file contains TEST_VAR=value
   - Check for permission issues
   ```

3. **Decide on action:**
   - **Fix now:** If it's a quick fix related to your changes
   - **Defer:** If it's a pre-existing issue unrelated to your work
   - **Document:** If it's a known limitation

4. **Don't commit if unit tests fail** (unless explicitly deferred)

---

## Non-Blocking vs Blocking

**Non-blocking (proceed with commit):**
- ⚠️ Integration tests timeout (external service slow)
- ⚠️ Code quality warnings (mypy, pylint)
- ⚠️ Coverage decreased slightly but still ≥60%
- ⚠️ Demo application needs credentials to fully test

**Blocking (don't commit):**
- ❌ Unit tests fail (pytest tests/ -v shows failures)
- ❌ Syntax errors (python -m py_compile src/file.py fails)
- ❌ Import errors (failed to import modified module)
- ❌ Real credentials in commit (git diff shows API keys)
- ❌ Merge conflicts or git errors

---

## Examples

### Example 1: Successful Completion

```
✅ DEFINITION OF DONE - COMPLETE

Phase 1: Formatting
  - black: ✅ 0 files reformatted
  - ruff --fix: ✅ 2 issues fixed

Phase 2: Unit Tests
  - pytest: ✅ 44 passed in 0.32s

Phase 3: Integration Tests
  - timeout 30 server help: ✅ OK
  - timeout 30 config load: ✅ OK

Phase 4: Code Quality
  - mypy: ⚠️ 3 warnings (logged, non-blocking)
  - pylint: ✅ No errors

Phase 5: Coverage
  - Coverage: 85% (target 60%) ✅

Phase 6: Review
  - git diff: ✅ All changes intentional
  - No credentials: ✅ Clean

Phase 7: Commit
  - Commit hash: a1b2c3d ✅
  - Message: "Add credential masking utility" ✅

Phase 8: Notification
  - Slack: ✅ Posted summary

Status: ✅ READY FOR MERGE
```

### Example 2: Partial Failure

```
⚠️ DEFINITION OF DONE - COMPLETED WITH WARNINGS

Phase 1: Formatting
  - black: ✅ OK
  - ruff: ✅ OK

Phase 2: Unit Tests
  ❌ FAILED: 1 test failing

  Test: tests/test_config.py::TestLoadEnvFile::test_load_env_file_basic
  Error: KeyError: 'TEST_VAR'
  Root cause: Test setup missing - env var not initialized
  Fix: Add monkeypatch.setenv('TEST_VAR', 'test_value') to test

  Status: BLOCKING - Do NOT commit
  Action: Fix the test or defer with explanation

Phase 3-8: Not reached (blocked at unit tests)

Status: ❌ CANNOT COMMIT - Fix failing test first
```

### Example 3: Integration Test Failure

```
✅ DEFINITION OF DONE - PARTIAL SUCCESS

Phase 1-2: ✅ All passed

Phase 3: Integration Tests
  ⚠️ timeout 30 google-personal-mcp server
     Exit code: 124 (timeout)

     Explanation: Server initialization takes >30 seconds

     Root cause: google-api-client library imports take time
     OR server tries to authenticate on startup

     Fix for next iteration:
     - Lazy-load Google API clients (don't on startup)
     - Mock Google APIs in test mode
     - Use environment variable to skip auth on startup

     Status: ⚠️ NON-BLOCKING (legitimate environmental issue)

Phase 4-7: ✅ All passed

Phase 8: Slack notification posted

Status: ✅ READY FOR MERGE (with note about integration test timing)

Note: Integration test timeout is non-blocking, but recommend
      investigating performance optimization for startup time
```

---

## Key Rules

1. **Always run unit tests** (`pytest tests/ -v`)
2. **Always format code** (`black` + `ruff --fix`)
3. **Always review changes** (`git diff --cached`)
4. **Always attempt integration tests** (with `timeout 30` protection)
5. **Always log failures** (with root cause analysis)
6. **Never commit with failing unit tests** (unless explicitly deferred)
7. **Never commit with real credentials** (check git diff!)
8. **Never skip documentation** (docstrings, commit messages)
9. **Always get human approval** (before final commit in interactive workflows)
10. **Always notify team** (Slack, when configured)

---

## Related Documents

- [AGENTS.md](./AGENTS.md) - Agent development index (links to this document)
- [contributing.md](./contributing.md) - Code style and commit message guidelines
- [mcp-development-guide.md](./mcp-development-guide.md) - Development reference
- [development.md](./development.md) - Architecture and patterns
- [troubleshooting.md](./troubleshooting.md) - Common issues

---

**Last Updated:** 2026-01-27
**Status:** Active
**Applies to:** All Python development on this project

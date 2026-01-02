# 🔄 Real-World Workflows

> **Complete, copy-paste examples for common coding tasks.**

This is what Reddit asked for: "Show me a real workflow, not just setup."

---

## Workflow 1: Debug a React Component

**Scenario**: Avatar doesn't update after profile picture change.

### Setup

```bash
# Ensure Ollama is running
ollama serve &

# Start Aider or Continue.dev
aider src/components/UserProfile.tsx src/components/UserProfile.test.tsx
```

### The Prompt

```
The avatar in <UserProfile /> doesn't update after changing the profile picture.

STEPS:
1. Read UserProfile.tsx and UserProfile.test.tsx
2. Run `npm test -- UserProfile.test.tsx`
3. Explain the bug in 3-5 bullet points
4. Propose a plan (3-5 steps)
5. Apply minimal changes
6. Re-run tests until they pass

CONSTRAINTS:
- Only modify UserProfile.tsx
- Do NOT change test files
- Keep public API the same
```

### Expected Flow

```
AGENT: Reading UserProfile.tsx... (300 lines)
AGENT: Reading UserProfile.test.tsx... (150 lines)
AGENT: Running npm test -- UserProfile.test.tsx

Test Results:
  ✗ should update avatar on image change (50ms)
    Expected: <img src="new-avatar.jpg" />
    Received: <img src="old-avatar.jpg" />

AGENT: Analysis:
  - The component uses useState for avatar
  - But useEffect doesn't re-run when profilePic prop changes
  - Missing dependency in useEffect array

PLAN:
  1. Add profilePic to useEffect dependencies
  2. Update avatar state when profilePic changes
  3. Run tests

APPLYING CHANGES...

AGENT: Running tests again...
  ✓ should update avatar on image change (45ms)

All tests passing. Ready for review.
```

### Review & Commit

```bash
git diff
git add -A
git commit -m "Fix: Avatar not updating on profile picture change"
```

---

## Workflow 2: Write a Python API Endpoint

**Scenario**: Add `/api/users/{id}` endpoint to FastAPI app.

### Setup

```bash
# With LM Studio server
aider app/api/users.py tests/test_users_api.py
```

### The Prompt

```
Add a new FastAPI GET endpoint `/api/users/{id}` in app/api/users.py.

REQUIREMENTS:
- Return 404 if user not found
- Use existing User model from app/models.py
- Use get_user_by_id() from app/db.py

TDD APPROACH:
1. First, write tests in tests/test_users_api.py
2. Run tests (they should fail)
3. Implement the endpoint
4. Run tests until they pass

CONSTRAINTS:
- Do NOT add new dependencies
- Follow existing code style
- Include docstrings
```

### Expected Flow

```
AGENT: Creating test file tests/test_users_api.py

```python
# tests/test_users_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_success():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_user_not_found():
    response = client.get("/api/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

AGENT: Running pytest tests/test_users_api.py
  ✗ test_get_user_success - 404 (endpoint doesn't exist)
  ✗ test_get_user_not_found - 404 (endpoint doesn't exist)

AGENT: Implementing endpoint in app/api/users.py

```python
# app/api/users.py
from fastapi import APIRouter, HTTPException
from app.models import User
from app.db import get_user_by_id

router = APIRouter()

@router.get("/api/users/{user_id}")
def get_user(user_id: int) -> User:
    """Get a user by ID. Returns 404 if not found."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

AGENT: Running tests...
  ✓ test_get_user_success (50ms)
  ✓ test_get_user_not_found (45ms)

Done! 2 tests passing.
```

---

## Workflow 3: Refactor Legacy Code

**Scenario**: Split a 500-line function into smaller units.

### Setup

```bash
# Use Plan mode first
aider --no-auto-commits src/legacy/big_function.py
```

### Step 1: Planning Phase

```
/ask This function process_order() is 500 lines and handles:
- Input validation
- Price calculation
- Inventory check
- Payment processing
- Email notification

Create a refactoring plan:
1. Identify logical subsections
2. Propose new helper functions with signatures
3. List steps to move code without changing behavior

DO NOT modify code yet.
```

### Expected Plan

```
REFACTORING PLAN for process_order():

HELPER FUNCTIONS TO CREATE:
1. validate_order(order: Order) -> ValidationResult
2. calculate_total(items: List[Item]) -> Decimal
3. check_inventory(items: List[Item]) -> InventoryStatus
4. process_payment(order: Order, amount: Decimal) -> PaymentResult
5. send_confirmation_email(order: Order) -> None

STEPS:
1. Create empty functions with signatures
2. Move validation logic (lines 45-120) to validate_order()
3. Move calculation logic (lines 121-200) to calculate_total()
4. Move inventory logic (lines 201-280) to check_inventory()
5. Move payment logic (lines 281-400) to process_payment()
6. Move email logic (lines 401-500) to send_confirmation_email()
7. Update process_order() to call helpers
8. Run tests after each step

Shall I proceed?
```

### Step 2: Execution (After Approval)

```
/code I approve the plan. Implement step by step.
Run `pytest tests/test_orders.py` after each major change.
Show diffs for each step.
```

### Safety Checkpoints

```bash
# After each step
git add -A
git commit -m "Refactor: Extract validate_order() from process_order()"

# Run tests
pytest tests/test_orders.py

# If tests fail, revert
git checkout HEAD~1 -- src/legacy/big_function.py
```

---

## Workflow 4: Code Review with AI

**Scenario**: Review a PR before merging.

### The Prompt

```
Review this diff for:

```diff
--- a/src/auth/middleware.ts
+++ b/src/auth/middleware.ts
@@ -45,7 +45,7 @@ export function authenticate(req, res, next) {
-  const token = req.headers.authorization;
+  const token = req.headers.authorization?.split(' ')[1];
   
   if (!token) {
-    return res.status(401).json({ error: 'No token' });
+    return res.status(401).json({ error: 'Unauthorized' });
   }
```

REVIEW FOR:
- Potential bugs
- Security issues
- Edge cases
- Breaking changes

Be specific. Quote line numbers.
```

### Expected Output

```
CODE REVIEW FINDINGS:

✅ GOOD CHANGES:
- Line 45: Now correctly extracts token from "Bearer <token>" format
- Line 48: More professional error message

⚠️ CONCERNS:

1. POTENTIAL BUG (Line 45):
   If authorization header is "Bearer" without a token,
   split(' ')[1] returns undefined, which passes the `if (!token)` check
   but will fail later.
   
   FIX: Add explicit length check
   ```ts
   const parts = req.headers.authorization?.split(' ');
   const token = parts?.length === 2 ? parts[1] : null;
   ```

2. BREAKING CHANGE (Line 48):
   Error message changed from "No token" to "Unauthorized".
   If any client code parses this message, it will break.
   
   RECOMMENDATION: 
   Add error code field: `{ error: 'Unauthorized', code: 'NO_TOKEN' }`

3. MISSING EDGE CASE:
   No validation that the header starts with "Bearer ".
   "Basic abc123" would extract "abc123" as a JWT token.

VERDICT: Request changes before merge.
```

---

---

## Workflow 5: The Debug Protocol (When Stuck)

**Scenario**: The agent is spinning in circles, fixing one bug but creating another.

### The "Reset & Isolate" Strategy

**1. The STOP Command**
Abruptly stop the current generation. Do not let it finish a bad thought.

**2. The Context Wipe**
```bash
/clear
```

**3. The Minimal Reproduction**
Create a new file `repro_bug.py` that isolates *only* the failing logic. No dependencies, no framework code.

```python
# repro_bug.py
# If this script fails, we found the core issue.
def broken_logic():
    ...
```

**4. The "Rubber Duck" Prompt (DeepSeek R1)**
Switch to your strongest reasoning model.

```
I am stuck on a logic bug.
Here is the isolated reproduction code: [repro_bug.py]
Here is the error: [error log]

Please perform a root cause analysis.
Do not write code yet. just Explain *why* it is failing.
Think step-by-step.
```

**5. The Zero-Shot Fix**
Once the reasoning model explains it, switch back to the coding model (Qwen/Claude) to apply the fix to the main codebase.

---

## Realistic Expectations

### Local Models Excel At (~70% of tasks)

| Task | Success Rate |
|------|:------------:|
| Bug fixes with clear errors | ✅ ~80% |
| Adding small features | ✅ ~75% |
| Writing tests | ✅ ~85% |
| Single-file refactors | ✅ ~70% |
| Documentation | ✅ ~90% |

### Local Models Struggle With

| Task | Success Rate |
|------|:------------:|
| Multi-file architectural changes | ❌ ~30% |
| Novel algorithms | ❌ ~20% |
| Ambiguous requirements | ❌ ~25% |
| Cross-repo reasoning | ❌ ~15% |

### The Hybrid Strategy

```
70% Local:
- Routine fixes
- Test writing
- Boilerplate
- Documentation

30% Cloud (When Needed):
- Complex architecture
- Novel problems
- Critical security code
```

---

## Troubleshooting Workflows

### Agent Gets Stuck

```
/clear  # Clear context
/add src/specific_file.py  # Add only relevant files
/ask [simpler, more specific prompt]
```

### Tests Keep Failing

```
Let's try a different approach.
Show me the EXACT test output.
What is the MINIMAL change that could fix this?
```

### Too Many Changes

```
STOP.
Revert all changes: git checkout -- .
Let's start over with a smaller scope.
Only modify {specific_file}.
```

---

## Next Steps

- [Runner Comparison](runner-comparison.md) — Pick the right engine
- [Guardrails](guardrails.md) — Prevent hallucinations
- [Prompt Engineering](prompt-engineering.md) — Better prompts

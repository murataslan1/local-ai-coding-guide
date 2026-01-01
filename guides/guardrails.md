# 🛡️ Guardrails & Coding Plans

> **How to prevent local models from hallucinating and breaking your code.**

Reddit feedback was clear: "The guide is 'end-to-end' but where are the guardrails?"

---

## The Core Problem

Local models (especially 7B-14B) are prone to:
- Hallucinating functions that don't exist
- Over-editing (changing files you didn't ask about)
- Ignoring edge cases
- Breaking working code while "fixing" it

**Solution**: Use tests, plans, and verification loops.

---

## Strategy 1: Unit Tests as Feedback Loop

The most effective guardrail is **Test-Driven Development (TDD)**.

### The TDD Loop

```
1. YOU write a failing test
2. AI implements code to pass the test
3. Test runs automatically
4. If fail → AI analyzes error, tries again
5. If pass → Move to next feature
```

### Example System Prompt

```
You are an AI developer practicing TDD.

RULES:
1. Read the failing test output first
2. Modify ONLY implementation files (never tests)
3. Make the MINIMUM change required to pass
4. If tests still fail, analyze the new error and try again
5. Stop when all tests pass

You may NOT:
- Add new dependencies
- Change test files
- Refactor unrelated code
```

### Implementation with Aider

```bash
# Create a failing test first
cat > test_calculator.py << 'EOF'
def test_add():
    from calculator import add
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
EOF

# Run Aider
aider calculator.py test_calculator.py

# Prompt
/ask The test test_add is failing because calculator.py doesn't exist yet.
Please:
1. Run `pytest test_calculator.py`
2. Implement calculator.py to pass the test
3. Run tests again until green
```

---

## Strategy 2: The "Coding Plan" Approach

**Before coding, make the model plan.**

This reduces hallucinations because:
- Planning forces the model to think before acting
- You can catch mistakes before they're implemented
- Plans are easier to verify than code

### The Two-Step Workflow

```
Step 1: PLAN (read-only)
───────────────────────
"Analyze the failing test. DO NOT write code yet.
Create a numbered plan with 3-7 steps describing what you will change."

Step 2: EXECUTE (after approval)
────────────────────────────────
"I approve the plan. Now implement step by step.
Show a diff for each step. Run tests after each major change."
```

### Plan Mode in Continue.dev

1. Select code in VS Code
2. Open Continue → Select "Plan" mode
3. Describe what you want
4. Review the plan
5. Switch to "Agent" mode to execute

---

## Strategy 3: Linting & Type Checking

Auto-verify AI output with static analysis.

### Integrate into Agent Workflow

```
After editing code, you MUST:
1. Run `ruff .` (Python) or `eslint .` (JS) and fix warnings
2. Run `mypy .` or `tsc --noEmit` and fix type errors
3. Only then consider the change complete
```

### Aider with Auto-Lint

```yaml
# ~/.aider.conf.yml
lint-cmd: "ruff check --fix"
auto-lint: true
```

---

## Strategy 4: Self-Verification Prompts

Make the model critique its own work.

### The "Explain Your Fix" Technique

```
After you apply the fix, explain:
1. What was the root cause?
2. Why does your change fix it?
3. What edge cases might still fail?
4. Rate your confidence (1-10)

If confidence < 7, reconsider your approach.
```

### The Dual-Pass Technique

```
Pass 1: Generate the fix

Pass 2: Critique prompt:
────────────────────────
"You are a senior engineer reviewing this diff.
List any:
- Potential bugs
- Unhandled edge cases
- Violations of requirements
- Security issues

Be critical. If you find issues, revise the code."
```

---

## Strategy 5: Scope Limiting

Never let the agent have free reign.

### Explicit File Constraints

```
RULES:
- Only modify: PaymentService.ts, PaymentService.test.ts
- Do NOT touch: config.ts, package.json, any .env files
- Do NOT add new files
```

### Git-Based Safety

```bash
# Before agent session
git stash
git checkout -b agent-experiment

# After session
git diff main  # Review all changes
git checkout main  # If bad, discard
```

---

## The Complete Guardrail Checklist

```
Before Agent Session:
☐ Git is clean (committed or stashed)
☐ Tests exist and pass
☐ Clear, specific prompt written
☐ Scope explicitly limited

During Session:
☐ Plan mode before Agent mode
☐ Tests run after each change
☐ Lint/type check passes
☐ Agent explains its changes

After Session:
☐ git diff reviewed
☐ All tests still pass
☐ No unexpected file changes
☐ Commit with descriptive message
```

---

## Quantization & Quality

Lower quantization = more hallucinations.

| Use Case | Minimum Quant | Recommended |
|----------|:-------------:|:-----------:|
| Autocomplete | Q4_K_M | Q4_K_M |
| Simple fixes | Q4_K_M | Q5_K_M |
| Complex refactors | Q5_K_M | Q6_K or Q8 |
| Architecture planning | Q5_K_M | Q8_0 |

> **Rule**: If you're doing critical refactoring, use the highest quantization your VRAM allows.

---

## Common Guardrail Failures

### ❌ "Just fix the bug"

Too vague. Model might:
- Change random files
- "Fix" by deleting code
- Introduce new bugs

### ✅ "Fix test_user_login by..."

```
Fix test_user_login, which fails with "401 Unauthorized".
The issue is likely in auth/middleware.ts lines 45-60.
Do NOT modify any other files.
Run `npm test -- test_user_login` after changes.
```

### ❌ No tests = No guardrails

Without tests, you're flying blind. The model can claim "fixed!" while your app is broken.

### ✅ Always have verification

```
After your change, prove it works:
1. Run `pytest`
2. Run `npm run lint`
3. Show me the passing output
```

---

## Next Steps

- [Prompt Engineering](prompt-engineering.md) — Better prompts for local models
- [Real-World Workflows](workflows.md) — Complete examples

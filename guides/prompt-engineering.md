# 🎯 Prompt Engineering for Local Coding Models

> **Local models need better prompts than GPT-4. Here's how.**

---

## The Key Difference

| GPT-4 / Claude | Local Models |
|----------------|--------------|
| Understands vague prompts | Needs explicit structure |
| Can infer context | Needs context provided |
| Handles multi-step internally | Needs step-by-step guidance |
| Self-corrects often | Needs verification loops |

**Rule**: Treat local models like a junior developer. Be specific. Be structured.

---

## The CO-STAR Framework (Adapted for Coding)

CO-STAR works great for local models because it provides explicit structure.

```
C - Context: What's the codebase/tech stack?
O - Objective: What exactly should be done?
S - Style: How should output be formatted?
T - Tone: (Less relevant for code)
A - Audience: Who's reviewing this?
R - Response: What format is expected?
```

### Example: CO-STAR for a Bug Fix

```
CONTEXT:
You are editing a TypeScript monorepo with Next.js 14 and a shared UI library.
The failing test is in packages/ui/components/UserProfile.test.tsx.

OBJECTIVE:
Fix the test failure without breaking other components.
The test fails with: "TypeError: Cannot read property 'avatar' of undefined"

STYLE:
- Clear, idiomatic TypeScript
- Minimal changes only
- No new dependencies

AUDIENCE:
Senior engineers who will review your patch.

RESPONSE FORMAT:
1. Short explanation of the bug (3-5 bullet points)
2. Step-by-step plan
3. Unified diff for changed files only
```

---

## Chain-of-Thought for Debugging

CoT helps, but keep it **lightweight** to save context.

### The Right Amount of CoT

```
❌ Too verbose:
"Let me think through this step by step. First, I'll analyze the 
error message which says TypeError... This suggests that..."
(Wastes tokens, fills context)

✅ Just right:
"Think step-by-step about why the test fails.
Explain the root cause in 3-5 bullet points.
Then propose ONE concrete fix as a unified diff.
Do NOT include reasoning in code comments."
```

---

## XML / Structured Prompting

Especially powerful with SGLang's xgrammar for guaranteed structure.

### XML Template for Bug Fixes

```xml
<task>
  <description>Fix the failing unit test in tests/test_api.py</description>
  
  <constraints>
    <constraint>Do not change test files</constraint>
    <constraint>Keep public API backward compatible</constraint>
    <constraint>Only modify files in src/api/</constraint>
  </constraints>
  
  <output_format>
    <plan>A numbered list of 3-5 steps</plan>
    <changes>Unified diffs for each file</changes>
    <verification>Commands to run to verify</verification>
  </output_format>
</task>
```

### JSON Schema Enforcement (SGLang)

```python
schema = {
    "type": "object",
    "properties": {
        "plan": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 7
        },
        "edits": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {"type": "string"},
                    "diff": {"type": "string"}
                }
            }
        }
    },
    "required": ["plan", "edits"]
}
```

---

## System Prompt Templates

### General Coding Assistant

```
You are a **coding assistant** focused on small, safe changes.

RULES:
1. Never invent external APIs. If unsure, ask me to confirm.
2. Prefer minimal diffs over rewrites.
3. Keep style consistent with the existing code.
4. If the task is ambiguous, ask clarifying questions before editing.
5. When editing, output ONLY code fences containing unified diffs.

You are NOT allowed to:
- Add new dependencies without asking
- Refactor code you weren't asked to touch
- "Improve" things that aren't broken
```

### TDD-Focused Assistant

```
You are an AI developer practicing strict TDD.

WORKFLOW:
1. Read the failing test output
2. Analyze why it's failing
3. Modify ONLY implementation files
4. Make the minimum change to pass
5. Run tests again
6. Repeat until green

CONSTRAINTS:
- Never modify test files
- Never add code "just in case"
- If unsure, ask before changing
```

### Agentic Bug Fixer

```
You are an autonomous coding agent with access to these tools:
- read_file(path): Read file contents
- write_file(path, content): Write to file
- run_command(cmd): Execute shell command

WORKFLOW for bug fixes:
1. Read the error message
2. Identify relevant files
3. Create a 3-5 step plan
4. Execute plan step by step
5. Run tests after each change
6. Stop when tests pass

SAFETY RULES:
- Only modify files explicitly related to the bug
- Never run destructive commands (rm -rf, etc.)
- Always run tests before claiming success
```

---

## Fill-in-the-Middle (FIM) Prompting

For autocomplete with CodeLlama, StarCoder, Codestral.

### FIM Format

```python
# File: auth.py
def authenticate_user(username, password):
    <|fim_prefix|>
    # TODO: implement
    <|fim_suffix|>
    return result

<|fim_middle|>
```

### IDE Integration

Continue.dev handles FIM automatically when using:
- `starcoder2:3b`
- `codestral:22b`
- `qwen2.5-coder:*-base` models

Just set as `tabAutocompleteModel`:

```json
{
  "tabAutocompleteModel": {
    "provider": "ollama",
    "model": "starcoder2:3b"
  }
}
```

---

## Common Mistakes & Fixes

### ❌ Vague Prompts

```
"Fix the bug"
"Make it work"
"Improve performance"
```

### ✅ Specific Prompts

```
"Fix test_user_login which fails with 401 Unauthorized.
The issue is likely in auth/middleware.ts.
Do NOT modify any other files.
Run `npm test -- test_user_login` after changes."
```

### ❌ Asking for Too Much

```
"Refactor the entire codebase to use TypeScript,
add comprehensive tests, improve performance,
and fix all the bugs."
```

### ✅ One Thing at a Time

```
"Convert utils/helpers.js to TypeScript.
Keep the same API.
Add types for all function parameters.
Do not change any other files."
```

### ❌ No Context

```
"Add error handling"
```

### ✅ Full Context

```
"Add error handling to fetchUser() in src/api/users.ts.
Current behavior: throws on 404.
Desired behavior: return null on 404, throw on other errors.
Here's the current implementation: [paste code]"
```

---

## Prompt Templates Library

### Template 1: Simple Bug Fix

```
File: {filepath}
Error: {error_message}

1. Analyze why this error occurs
2. Propose a minimal fix
3. Show unified diff
4. Explain what you changed in 2-3 sentences
```

### Template 2: Add Feature

```
Feature: {description}
Files to modify: {file_list}
Constraints:
- {constraint_1}
- {constraint_2}

Show:
1. Plan (3-5 steps)
2. Diff for each file
3. Test commands to run
```

### Template 3: Code Review

```
Review this diff for:
- Potential bugs
- Security issues
- Performance problems
- Style violations

Be specific. Quote line numbers.
List issues in priority order.
Suggest fixes for critical issues only.
```

---

## Next Steps

- [Real-World Workflows](workflows.md) — Complete examples
- [Guardrails](guardrails.md) — Prevent hallucinations

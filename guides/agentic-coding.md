# 🤖 Agentic Coding with Local Models

> **Turn your local LLM into an autonomous coding agent that reads, writes, tests, and iterates.**

This was the #1 requested feature from Reddit: "Show me a real workflow, not just setup."

---

## The Agentic Coding Stack

```
┌─────────────────────────────────────────────────────┐
│                   YOUR IDE                          │
│        (VS Code + Continue.dev or Aider)            │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│               INFERENCE ENGINE                       │
│        (Ollama / llama.cpp / vLLM)                  │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                 LOCAL MODEL                          │
│    (Qwen2.5-Coder-32B / DeepSeek-Coder-V2)          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   TOOLS                              │
│   read_file | write_file | run_command | git        │
└─────────────────────────────────────────────────────┘
```

---

## Option 1: Aider + Ollama (Terminal-First)

Aider is a terminal-based AI pair programmer. It's perfect for "I have a bug → fix it" workflows.

### Setup

```bash
# Install Aider
pip install aider-chat

# Create config file
cat > ~/.aider.conf.yml << 'EOF'
model: ollama/qwen2.5-coder:32b
openai-api-base: http://localhost:11434/v1
openai-api-key: "ollama"
auto-commits: false
EOF
```

### Usage

```bash
# Start Ollama
ollama serve &

# Run Aider in your repo
cd /path/to/project
aider .
```

### The "Bug Fix" Workflow

```
YOU: Tests `test_user_login` and `test_user_logout` are failing. Please:
     1) Run `pytest tests/test_auth.py`
     2) Read the failing tests and source files
     3) Propose a plan to fix
     4) Apply minimal changes
     5) Run tests again until they pass

AIDER: [Reads files, proposes patch, applies, runs tests, iterates...]

YOU: git diff  # Review changes
YOU: git commit -am "Fix auth login/logout bug"
```

---

## Option 2: Continue.dev Agent Mode (VS Code)

Continue.dev has three modes:
- **Chat**: Ask questions
- **Plan**: See what it intends to do
- **Agent**: Let it take action

### Configuration

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Qwen 32B (Agent)",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b"
    }
  ],
  "tabAutocompleteModel": {
    "title": "StarCoder2 3B",
    "provider": "ollama",
    "model": "starcoder2:3b"
  },
  "allowAnonymousTelemetry": false
}
```

### Agent Mode Tools

When you enable Agent mode, Continue can use:

| Tool | What It Does |
|------|--------------|
| `read_file` | Read any file in workspace |
| `write_file` | Create or modify files |
| `run_command` | Execute shell commands |
| `run_tests` | Run test suites |
| `search_codebase` | Find relevant code |

### The "Fix Bug" Workflow

1. Open failing file in VS Code
2. Open Continue sidebar → Select Agent mode
3. Prompt:

```
The avatar in <UserProfile /> doesn't update after changing the profile picture.

1) Read the component and its tests
2) Run `npm test -- UserProfile.test.tsx`
3) Explain the bug in 3-5 bullet points
4) Propose a plan
5) Apply minimal code changes
6) Re-run tests until they pass
```

4. Let Agent iterate
5. Review diffs and approve

---

## Option 3: OpenDevin / SWE-Agent with Local Models

For fully autonomous agents that work like a junior developer.

### Setup with vLLM Backend

```bash
# Start vLLM server
vllm serve Qwen/Qwen2.5-Coder-32B-Instruct --port 8000

# Configure environment
export OPENAI_API_BASE=http://localhost:8000/v1
export OPENAI_API_KEY="local"
export OPENAI_MODEL="qwen2.5-coder-32b"

# Run SWE-Agent
python -m swe_agent.run \
  --model_name qwen2.5-coder-32b \
  --issue "Fix the failing CI tests in auth module"
```

> ⚠️ **Warning**: These agents can modify many files. Always use in a sandboxed environment or with git worktrees.

---

## The Complete "Bug Fix" Workflow

Here's a step-by-step example with Aider + Ollama:

### Step 1: Start Fresh

```bash
# Ensure repo is clean
git status
git stash  # if needed

# Start Aider
aider .
```

### Step 2: Describe the Bug

```
/ask The test `test_payment_processing` is failing with "TypeError: 
Cannot read property 'amount' of undefined". 

Please:
1. Run `npm test -- test_payment_processing`
2. Read the test file and the PaymentService.ts
3. Explain why this error occurs
4. Create a 3-step plan to fix it
```

### Step 3: Approve the Plan

Aider will output something like:

```
PLAN:
1. Add null check in PaymentService.processPayment()
2. Handle edge case when payment.amount is undefined
3. Add defensive test case

Shall I proceed? [y/n]
```

### Step 4: Let It Fix

```
/code Implement step 1 of the plan. Show me the diff before applying.
```

### Step 5: Test & Iterate

```
/run npm test -- test_payment_processing
```

If tests still fail, Aider will analyze and try again.

### Step 6: Commit

```bash
git diff
git add -A
git commit -m "Fix: Handle undefined amount in PaymentService"
```

---

## Multi-File Editing Best Practices

Local models struggle with massive refactors. Here's how to succeed:

### Do's ✅

```
✅ Limit scope: "Only modify PaymentService.ts and its tests"
✅ Use tests as guardrails: "Run tests after each change"
✅ Short sessions: Restart agent when context gets polluted
✅ Plan first: Use Plan mode before Agent mode
✅ Be specific: "Add null check on line 45" vs "fix the bug"
```

### Don'ts ❌

```
❌ "Refactor the entire codebase"
❌ "Add feature X, Y, Z, and also fix bugs A, B, C"
❌ Running for hours without checkpoints
❌ Skipping the planning step
❌ Ignoring test failures
```

---

## Realistic Expectations

### Local Models Can Do (~70% of coding tasks)

- ✅ Bug fixes with clear error messages
- ✅ Adding small features
- ✅ Writing tests for existing code
- ✅ Refactoring single files
- ✅ Documentation generation
- ✅ Boilerplate reduction

### Local Models Struggle With

- ❌ Large architectural redesigns
- ❌ Cross-repository changes
- ❌ Highly ambiguous requirements
- ❌ Novel algorithms without examples
- ❌ Multi-step reasoning over 10+ files

### The Hybrid Strategy

```
70% Local → Routine tasks, boilerplate, small fixes
30% Cloud → Complex architecture, multi-file reasoning
```

---

## Troubleshooting

### Agent Gets Stuck in Loop

```bash
# Restart with fresh context
/clear
/add <specific files only>
```

### Agent Ignores Instructions

Add explicit constraints:

```
RULES:
- Do NOT modify test files
- Do NOT add new dependencies
- Only change PaymentService.ts
```

### Agent Runs Dangerous Commands

In Continue.dev settings:
```json
{
  "disableAutoRun": true,
  "allowedCommands": ["npm test", "npm run lint"]
}
```

---

## Next Steps

- [Guardrails & Coding Plans](guardrails.md) — Prevent hallucinations
- [Prompt Engineering](prompt-engineering.md) — Better results from local models
- [Real-World Workflows](workflows.md) — Complete examples

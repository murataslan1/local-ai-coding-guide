# 🏗️ Advanced Patterns & Strategies

> **Expert-level workflows for maximizing local AI coding productivity.**

Source: Community research and professional developer reports (December 2025 - January 2026).

---

## 🎭 The "Reasoning" vs "Instruct" Model Split

The most important insight of late 2025: **You need TWO types of models.**

| Feature | Reasoning Models | Instruct Models |
|---------|:----------------:|:---------------:|
| **Example** | DeepSeek-R1-Distill-32B | Qwen2.5-Coder-32B |
| **Primary Role** | Planning, Architecture | Code Generation, Refactoring |
| **Workflow Phase** | "Architect Mode" | "Code Mode" |
| **Strengths** | Self-correction, Logic | Instruction following, Speed |
| **Weaknesses** | Verbose, Slow, "Chatty" | Can hallucinate complex logic |
| **User Verdict** | "Smarter but slower" | "Reliable workhorse" |

### Why This Matters

```
❌ Using one model for everything = Suboptimal results

✅ R1 for planning → Qwen for execution = Best of both worlds
```

---

## 🧠 The Architect-Builder Pattern

This is THE workflow pattern emerging from the community.

### Phase 1: The Architect (Reasoning Model)

```
Tool: Roo Code / Aider (Architect Mode)
Model: DeepSeek-R1-Distill-32B

Prompt:
"We need to migrate the user database from SQLite to Postgres.
Analyze the codebase, identify dependencies, and draft a detailed
migration_plan.md specification. Do NOT write code yet.
Identify potential risk areas and update the Memory Bank."
```

**What happens**: The reasoning model thinks through the problem, creates a plan, identifies risks.

### Phase 2: The Builder (Instruct Model)

```
Tool: Roo Code / Aider (Code Mode)
Model: Qwen2.5-Coder-32B

Prompt:
"Execute Phase 1 of migration_plan.md.
Generate SQL scripts, update ORM definitions, refactor connection logic."
```

**What happens**: The fast instruct model executes the plan efficiently.

### Phase 3: The Auditor (Automated + Human)

```bash
# Run tests
npm test

# If failures, feed errors back to Builder
aider --error-log test_failures.log
```

**Why it works**: Leverages R1's "IQ" for planning without suffering from slowness during coding.

---

## 📝 Roo Code Memory Bank System

Roo Code (formerly Cline) solves the context window problem with a **file-based memory system**.

### The Memory Bank Structure

```
project-root/
├── .roo/
│   ├── activeContext.md    # Current focus
│   ├── productContext.md   # Product requirements
│   ├── decisionLog.md      # Why decisions were made
│   └── techStack.md        # Technologies used
├── src/
└── ...
```

### How It Works

1. Model reads Memory Bank at start of session
2. Updates it as decisions are made
3. Retrieves context on demand, not all at once
4. Works around 16k-32k effective context limits

### Example Memory Bank Entry

```markdown
<!-- activeContext.md -->
# Current Focus

## Active Task
Migrating authentication from sessions to JWT

## Files Being Modified
- src/auth/middleware.ts
- src/auth/jwt.ts (new)
- tests/auth.test.ts

## Key Decisions
- Using jose library for JWT (smaller than jsonwebtoken)
- Refresh tokens stored in httpOnly cookies

## Next Steps
1. Implement token refresh logic
2. Update all protected routes
3. Add integration tests
```

---

## 🚀 YOLO Mode: Fully Autonomous Agents

For developers who trust their tests, **YOLO Mode** auto-approves all AI actions.

### The Setup

```bash
# Create isolated container
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  node:20 bash

# Inside container, run agent with YOLO
aider --yes-always .
```

### The Workflow

```
1. Spin up dev container
2. Mount repo (read-write)
3. Initialize agent with high-level goal
4. Agent runs autonomously for hours
5. Developer reviews final result
```

### Example YOLO Goal

```
"Increase test coverage to 80%.
Write tests for all untested functions.
Run tests after each file.
Fix any failures.
Commit when all tests pass."
```

### ⚠️ Critical Safety Rules

```
✅ ALWAYS use containers (Docker/Podman)
✅ NEVER run YOLO on bare metal
✅ Limit file system access
✅ Disable network access if possible
✅ Review git diff before pushing

Horror stories:
- Agent ran `rm -rf` on production repo
- Agent executed database reset command
- Agent committed API keys
```

---

## 📖 Documentation-Driven Development (DDD)

Local models struggle with "read the code and fix it." Invert the process.

### The Traditional (Broken) Approach

```
1. Ask AI to read codebase
2. Ask AI to implement feature
3. Result: Hallucinations, wrong assumptions
```

### The DDD Approach

```
1. Generate code summary/map
2. Update ARCHITECTURE.md with desired state
3. Ask AI to make code conform to documentation
4. Result: Aligned expectations, better output
```

### Step-by-Step

**Step 1: Generate Summary**

```bash
# Use aider's repo map feature
aider --show-repo-map > ARCHITECTURE.md
```

**Step 2: Update Documentation**

```markdown
<!-- ARCHITECTURE.md -->
# Authentication Module

## Current State
- Uses session-based auth
- Sessions stored in Redis

## Desired State
- JWT-based auth
- Stateless, no Redis dependency
- Refresh tokens in httpOnly cookies

## Migration Plan
1. Add jwt.ts utility
2. Modify middleware.ts
3. Remove Redis dependency
4. Update tests
```

**Step 3: Implement to Match Docs**

```
Prompt: "Make the code in src/auth/ conform to the
Desired State described in ARCHITECTURE.md."
```

**Why it works**: The model has clear, explicit context about what you want.

---

## 🔀 Model Router Architecture

Simulate Mixture-of-Experts at the application layer.

### Roo Code Mode Configuration

```json
{
  "modes": {
    "architect": {
      "model": "ollama/deepseek-r1:32b",
      "purpose": "Planning, debug, architecture"
    },
    "code": {
      "model": "ollama/qwen2.5-coder:32b",
      "purpose": "Implementation, refactoring"
    },
    "autocomplete": {
      "model": "ollama/qwen2.5-coder:1.5b-base",
      "purpose": "Fast ghost text"
    }
  }
}
```

### Decision Logic

```
IF task is "plan", "design", "debug", "analyze":
  → Use Reasoning Model (R1)

IF task is "write", "refactor", "implement", "fix":
  → Use Instruct Model (Qwen)

IF task is "complete", "autocomplete":
  → Use Small Fast Model (1.5B)
```

---

## 📊 The "Apply" Problem

The biggest friction point in AI coding: **merging generated code into files**.

### The Problem

```
AI generates: "Replace lines 45-60 with..."
IDE tries to match, but:
- Indentation differs
- Whitespace differs
- Code changed since analysis
- "Apply" fails, human intervention needed
```

### Why Qwen Beats R1 for "Apply"

| Model | Apply Success Rate | Why |
|-------|:------------------:|-----|
| **Qwen 32B** | ~95% | Trained on diffs, concise output |
| **R1 32B** | ~70% | "Overthinks", adds commentary |

### Improve Apply Success

```
PROMPT ADDITION:
"Output ONLY the replacement code.
No explanations before or after.
Match existing indentation exactly.
Do not modify unrelated lines."
```

---

## 🛡️ The 24GB "Hard Deck"

Community consensus: **24GB is the minimum for professional local AI coding.**

### Hardware Tiers

| Tier | Memory | Capability |
|------|:------:|------------|
| **Entry** | 16GB | Autocomplete only, 7B models |
| **Pro** | 24GB | Full 32B Q4, professional daily driver |
| **Enthusiast** | 48GB | 70B models, dual-GPU |
| **Research** | 128GB+ | 671B frontier models |

### 24GB Reality Check (M4 Pro)

| Quantization | VRAM Used | System Impact |
|:-------------|:---------:|---------------|
| Q4_0 | 21GB | High memory pressure |
| Q4_K_S | 22GB | Critical, close other apps |
| IQ4_XS | 20GB | Balanced, browser ok |
| IQ3_XXS | 19GB | Good headroom, quality drop |

> "16GB is autocomplete territory. For real agentic coding, you need 24GB minimum. The quality jump at 32B is massive."
> 
> — Community consensus, December 2025

---

## 🔧 Recommended Tool Stack (January 2026)

| Use Case | Tool | Model | Benefit |
|----------|------|-------|---------|
| **Architecture** | Roo Code (Architect) | R1-Distill-32B | "System 2" reasoning |
| **Mass Refactoring** | Aider | Qwen 32B | Speed + Git integration |
| **Autocomplete** | Tabby / Continue | Qwen 1.5B | Sub-50ms latency |
| **Complex Debug** | Roo Code (Debug) | R1-Distill-70B | Large context |
| **Legacy Modernization** | Aider + Repo Map | Qwen 32B | Context-aware updates |

---

## 🎯 Key Takeaways

1. **Split your models**: Reasoning for planning, Instruct for coding
2. **Use Memory Banks**: Persistent context across sessions
3. **YOLO in containers only**: Never on bare metal
4. **DDD works**: Document first, code second
5. **24GB minimum**: For professional agentic coding
6. **Qwen for Apply**: Better diff generation than R1
7. **Router architecture**: Right model for each task

# ⚠️ Gotchas & Common Mistakes

> **What goes wrong when switching from Copilot to local models.**

This section is based on real issues reported by the r/LocalLLaMA community.

---

## Top 10 Mistakes

### 1. Expecting GPT-4 Quality from 7B Models

**The Mistake**: "I tried Qwen 7B and it's terrible. Local AI sucks."

**Reality**: 
- 7B models are ~80% of GPT-4 on simple tasks
- 32B models reach ~90%+
- But local models need better prompts

**Fix**: 
- Use larger models for complex tasks
- Provide more structured prompts
- Lower expectations for edge cases

---

### 2. Dumping Entire Codebase into Context

**The Mistake**: Pasting 50,000 lines of code as "context."

**What Happens**:
- Model overwhelmed
- Slow inference
- Hallucinations increase
- OOM crashes

**Fix**:
```
❌ "Here's my entire repo. Fix the bugs."

✅ "Here are the 3 relevant files:
   - src/auth/login.ts (the bug is here)
   - src/auth/types.ts (dependencies)
   - tests/auth.test.ts (failing test)
   Fix the test_login failure."
```

---

### 3. Using the Wrong Quantization

**The Mistake**: Running Q2_K to "fit more" on GPU.

**Quality Degradation**:

| Quant | Quality | Coding Usability |
|-------|:-------:|:----------------:|
| Q8_0 | 100% | ✅ Perfect |
| Q6_K | ~98% | ✅ Excellent |
| Q5_K_M | ~95% | ✅ Great |
| **Q4_K_M** | **~90%** | **✅ Good** (default) |
| Q3_K | ~80% | ⚠️ Some issues |
| Q2_K | ~60% | ❌ Logic breaks |

**Fix**: 
- Use Q4_K_M as minimum for coding
- Use Q5+ for complex refactoring
- Accept smaller model over worse quant

---

### 4. Long Sessions Without Restarting

**The Mistake**: Running agent for hours without clearing context.

**What Happens**:
- Context pollution
- Model "forgets" earlier constraints
- Contradictory behavior
- KV cache bloat

**Fix**:
```bash
# After every major task
/clear  # Clear conversation

# Or restart completely
ollama stop qwen2.5-coder:32b
ollama run qwen2.5-coder:32b
```

---

### 5. No Tests = No Guardrails

**The Mistake**: "Fix the payment bug" with no tests.

**What Happens**:
- Model claims success
- Bug might be fixed
- But new bugs introduced
- No way to verify

**Fix**:
```
ALWAYS include verification:
1. Write test first (or ensure tests exist)
2. Agent fixes until tests pass
3. Run full test suite before commit
```

---

### 6. Using Chat Models for Autocomplete

**The Mistake**: Using `qwen2.5-coder:32b` (instruct) for tab completion.

**What Happens**:
- Slow (model is too big)
- Wrong format (tries to explain, not complete)
- Wastes resources

**Fix**:
```json
{
  "models": [{
    "title": "Qwen 32B (Chat)",
    "model": "qwen2.5-coder:32b"
  }],
  "tabAutocompleteModel": {
    "title": "Qwen 1.5B (Fast)",
    "model": "qwen2.5-coder:1.5b-base"  // BASE, not instruct
  }
}
```

---

### 7. Ignoring Memory Management

**The Mistake**: Running multiple models without monitoring.

**Symptoms**:
- Sudden slowdowns
- OOM crashes
- GPU fans at 100%

**Fix**:
```bash
# Check what's running
ollama ps

# Check GPU usage
nvidia-smi -l 1  # Updates every second

# Unload unused models
ollama stop unused-model

# Set memory limits
export OLLAMA_MAX_VRAM=22G
```

---

### 8. Vague Prompts

**The Mistake**:
```
"The code doesn't work, fix it"
"Improve performance"
"Make it better"
```

**Fix**:
```
"Fix test_user_login which fails with 'undefined password'.
The error is in auth/login.ts line 45.
Only modify that file.
Run `npm test -- login` to verify."
```

---

### 9. Mixing Models Mid-Conversation

**The Mistake**: Starting with Qwen, switching to DeepSeek mid-task.

**What Happens**:
- Different models have different "memory" formats
- Context from model A doesn't transfer to model B properly
- Inconsistent behavior

**Fix**:
- One model per task
- If switching, start a new conversation
- Same model for plan AND execute

---

### 10. Trusting Without Verifying

**The Mistake**: Accepting AI output without review.

**Real Horror Stories**:
```
- "Fixed the bug" → deleted the entire function
- "Improved security" → removed authentication
- "Optimized query" → infinite loop
```

**Fix**:
```bash
# ALWAYS review before commit
git diff

# ALWAYS run tests
npm test

# NEVER auto-commit agent changes
# (disable in aider: auto-commits: false)
```

---

## Environment-Specific Gotchas

### macOS

```bash
# Issue: Model runs on CPU instead of GPU
# Fix: Increase GPU allocation
sudo sysctl iogpu.wired_limit_mb=32000
```

### Windows

```bash
# Issue: Path length limits
# Fix: Enable long paths or use shorter paths

# Issue: WSL CUDA issues
# Fix: Use native Windows Ollama
```

### Linux

```bash
# Issue: Driver mismatch
nvidia-smi  # Check driver version
nvcc --version  # Check CUDA version

# Fix: Match CUDA version to driver
# Or use container with correct drivers
```

---

## Context Window Exhaustion

### Symptoms

- Model starts repeating itself
- Responses become incoherent
- "I've already explained this"
- Sudden quality drop

### Diagnosis

```
Total context = System prompt + Conversation history + Current request

If Total > Model's limit → Exhaustion
```

### Solutions

```bash
# 1. Check model's context
ollama show qwen2.5-coder:32b | grep context

# 2. Increase context (costs VRAM)
# Create custom modelfile
FROM qwen2.5-coder:32b
PARAMETER num_ctx 32768

# 3. Start fresh more often
/clear

# 4. Summarize before continuing
"Here's what we've done so far: [summary]
Continue from here."
```

---

## Performance Degradation Over Time

### Causes

1. **KV cache bloat**: Long conversations fill GPU memory
2. **Memory leaks**: Some runners leak slowly
3. **Thermal throttling**: GPU overheating

### Solutions

```bash
# Daily restart
systemctl restart ollama  # or just restart the app

# Monitor temperature
nvidia-smi -l 1 | grep Temp

# Cap concurrent sessions
# In ollama config, limit parallel contexts
```

---

## Quick Recovery Checklist

When things go wrong:

```
1. [ ] Stop the agent: /stop or Ctrl+C
2. [ ] Check git status: git status
3. [ ] Review changes: git diff
4. [ ] Revert if bad: git checkout -- .
5. [ ] Clear context: /clear
6. [ ] Restart with simpler prompt
7. [ ] Use smaller scope
```

---

## Next Steps

- [Runner Comparison](runner-comparison.md) — Pick the right engine
- [Guardrails](guardrails.md) — Prevent these issues
- [Prompt Engineering](prompt-engineering.md) — Better prompts

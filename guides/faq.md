# ❓ Frequently Asked Questions (FAQ)

> **Quick answers to the most common questions about local AI coding.**

---

## 🚀 Getting Started

### Q: What's the minimum hardware to run local coding AI?
**A:** 
- **Bare minimum**: 16GB RAM, any CPU from 2018+ → 7B models only
- **Recommended**: 24GB VRAM GPU (RTX 3090/4090) or 32GB RAM Mac → 32B models
- **Sweet spot**: RTX 3090 (24GB) - can be found used for $700-900

### Q: Which model should I start with?
**A:** 
- **Beginners**: `qwen2.5-coder:7b` (works on most hardware)
- **Standard**: `qwen2.5-coder:32b` (best balance)
- **Best quality**: `qwen2.5-coder:32b-instruct-q8_0` (if VRAM allows)

### Q: Is local AI as good as GitHub Copilot?
**A:** It can replace **60-80%** of Copilot functionality. Local excels at:
- ✅ Autocomplete (faster - no network latency)
- ✅ Targeted edits and refactoring
- ✅ Boilerplate generation
- ⚠️ Struggles with: Large codebase navigation, complex multi-file refactors

---

## 🔧 Technical Questions

### Q: Ollama vs LM Studio - which should I use?
**A:**
| Use Case | Choose |
|----------|--------|
| Developer, CLI lover | **Ollama** |
| Beginner, GUI preferred | **LM Studio** |
| Production/scripting | **Ollama** |
| Model comparison/testing | **LM Studio** |

Ollama is 20% faster with lower memory usage. LM Studio is easier to set up.

### Q: What quantization should I use (Q4, Q6, Q8)?
**A:**
- **Q8**: Best quality, use if VRAM allows
- **Q6**: Good balance
- **Q4**: Minimum for coding (below this, logic breaks)
- **Never use Q2/Q3** for coding tasks

> **Pro tip**: For coding, prioritize higher quant over bigger model.  
> `32B Q8` > `72B Q4` for coding efficiency

### Q: Why is my model slow/laggy?
**A:** Common causes:
1. **Model too big**: Reduce to smaller model or higher quant
2. **Memory pressure**: Close other apps, especially browsers
3. **CPU offloading**: Model doesn't fit in VRAM, using slow RAM
4. **Ollama running long**: Restart Ollama (`ollama stop && ollama serve`)

### Q: How do I increase context window?
**A:**
```bash
cat << 'EOF' > Modelfile
FROM qwen2.5-coder:32b
PARAMETER num_ctx 32768
EOF
ollama create qwen32k -f Modelfile
```

---

## 🤖 Workflow Questions

### Q: How do I prevent AI hallucinations?
**A:**
1. **Use TDD**: Write tests first, let AI implement to pass
2. **Plan before code**: Ask for a plan, then execute
3. **Limit scope**: Specify exactly which files to modify
4. **Review everything**: Never merge unreviewed AI code
5. **Clear context**: Start fresh sessions for new tasks

### Q: Agent mode doesn't work well - why?
**A:** Agent mode requires powerful models:
- **7B models**: Agent mode is essentially unusable
- **14B models**: Basic agent tasks only
- **32B models**: Full agent capability
- **70B models**: Best agent performance

### Q: Should I use Aider or Continue.dev?
**A:**
| You Prefer... | Choose |
|---------------|--------|
| Terminal workflows | **Aider** |
| VS Code GUI | **Continue.dev** |
| Git-first approach | **Aider** |
| Flexibility with providers | **Continue.dev** |

Many power users use both - Aider for heavy lifting, Continue for quick edits.

### Q: How to use reasoning models for coding?
**A:** The **Architect-Builder** pattern:
1. Use **DeepSeek R1** to create a plan
2. Switch to **Qwen Coder** to implement the plan
3. This gives you R1's "thinking" + Qwen's speed

---

## 💰 Cost Questions

### Q: Is local AI actually cheaper than cloud?
**A:**
| Factor | Cloud (GPT-4o) | Local (RTX 4090) |
|--------|:--------------:|:----------------:|
| Monthly cost | $200-500 | $0 |
| Hardware | $0 | ~$1,800 one-time |
| Break-even | - | 4-9 months |
| Electricity | $0 | ~$50-100/month |

**Break-even**: 3-12 months for heavy users (10,000+ requests/month)

### Q: Should I buy RTX 4090 or 5090?
**A:** 
- **RTX 4090**: Best value, 24GB VRAM, well-supported
- **RTX 5090**: 32GB VRAM, but marginal speed increase for LLMs
- **RTX 3090 (used)**: Best budget option ($700-900)

### Q: Mac or PC for local AI?
**A:**
| Choose Mac if... | Choose PC if... |
|------------------|-----------------|
| Need to run 70B+ models | Speed is priority |
| Want energy efficiency | Budget-conscious |
| Already in Apple ecosystem | Want raw performance |
| Prefer quiet operation | Need multi-GPU option |

---

## 🔒 Privacy Questions

### Q: Is my code really private with local models?
**A:** Yes, if you:
- ✅ Run Ollama locally (no external API calls)
- ✅ Disable telemetry in Continue.dev
- ✅ Don't use cloud features in Cursor/other tools
- ⚠️ Be careful: Some tools still make auth/update calls

### Q: Can I use local AI in air-gapped environments?
**A:** Yes, but requires extra setup:
1. Download models on connected machine
2. Transfer to air-gapped machine
3. Run Ollama in fully offline mode
4. Use Continue.dev (not Cursor which needs auth)

---

## 🐛 Troubleshooting

### Q: "Error: model not found"
**A:**
```bash
# List available models
ollama list

# Pull the model
ollama pull qwen2.5-coder:32b
```

### Q: Continue.dev not connecting to Ollama
**A:**
1. Ensure Ollama is running: `ollama serve`
2. Check port: `curl http://localhost:11434/api/tags`
3. Verify config.json has correct provider settings
4. Restart VS Code

### Q: Model keeps crashing mid-response
**A:** Usually OOM (Out of Memory):
1. Reduce `num_ctx` (context window)
2. Use smaller model or higher quantization
3. Close other applications
4. Monitor with `nvidia-smi` (Windows/Linux) or Activity Monitor (Mac)

### Q: Autocomplete is slow or laggy
**A:**
1. Use small model for autocomplete: `qwen2.5-coder:1.5b-base`
2. Reduce context length for autocomplete
3. Consider Tabby for dedicated autocomplete (sub-50ms latency)

---

## 📚 More Resources

- [Full Guide →](../README.md)
- [Agentic Coding →](./agentic-coding.md)
- [Guardrails →](./guardrails.md)
- [Troubleshooting →](./gotchas.md)
- [Community Experiences →](./community-experiences.md)

---

*Last updated: January 2026*

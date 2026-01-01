# 🖥️ LM Studio & Alternative Tools

> **GUI-first alternatives and specialized servers for local AI coding.**

---

## LM Studio: The Visual Explorer

LM Studio is a desktop application that provides a polished GUI for running local LLMs.

### When to Choose LM Studio Over Ollama

| Scenario | LM Studio | Ollama |
|----------|:---------:|:------:|
| Visual model comparison | ✅ | ❌ |
| Non-technical users | ✅ | ❌ |
| Scripting/automation | ❌ | ✅ |
| CI/CD integration | ❌ | ✅ |
| Cross-platform CLI | ❌ | ✅ |
| Model preset management | ✅ | Limited |

### Key Features

- **GUI Model Browser**: Browse Hugging Face, download models visually
- **Side-by-Side Comparison**: Compare outputs from different models/quantizations
- **Context Window Visualization**: See how much context you're using
- **OpenAI-Compatible Server**: Developer mode exposes localhost API

### Quick Setup

1. Download from [lmstudio.ai](https://lmstudio.ai/)
2. Search for "Qwen2.5-Coder-32B"
3. Download Q4_K_M quantization
4. Start local server (Developer Mode)
5. Point your tools to `http://localhost:1234/v1`

### API Configuration

```bash
# For Aider
export OPENAI_API_BASE=http://localhost:1234/v1
export OPENAI_API_KEY="lmstudio"
aider --model lmstudio/qwen2.5-coder:32b
```

---

## Tabby: Self-Hosted Code Completion

Tabby is **purpose-built for autocomplete**, not chat. It's designed to replace GitHub Copilot.

### Why Tabby for Autocomplete?

| Metric | Tabby | Ollama (Chat) |
|--------|:-----:|:-------------:|
| FIM (Fill-in-Middle) | ✅ Native | Via client |
| Latency target | <100ms | ~200-500ms |
| IDE integration | ✅ Deep | Via Continue |
| Memory footprint | Optimized | Standard |

### Architecture

```
┌─────────────────────────────────────┐
│           Tabby Server              │
│    (Optimized for completions)      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  StarCoder2 / Qwen-Base     │   │
│  │  (Non-instruct models)      │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
                ▲
                │ WebSocket (low latency)
                ▼
┌─────────────────────────────────────┐
│    IDE Extension (VS Code, JB)      │
│    "Ghost text" completions         │
└─────────────────────────────────────┘
```

### Docker Setup

```bash
# Start Tabby server
docker run -d \
  --name tabby \
  --gpus all \
  -p 5000:5000 \
  tabbyml/tabby \
  serve --model StarCoder2-3B

# Verify
curl http://localhost:5000/v1/health
```

### IDE Integration

1. Install Tabby extension in VS Code
2. Configure server URL: `http://localhost:5000`
3. Start typing – ghost text appears

### Model Recommendations for Tabby

| Model | Size | Use Case |
|-------|:----:|----------|
| StarCoder2-3B | 3B | Fast, general completion |
| Qwen2.5-Coder-1.5B-Base | 1.5B | Ultra-fast, small footprint |
| Codestral-22B | 22B | High-quality FIM |
| DeepSeek-Coder-6.7B-Base | 6.7B | Balanced quality/speed |

> **Important**: Use **Base** models, not Instruct, for autocomplete.

---

## Other Tools: Jan, GPT4All, LocalAI

### Jan

- **What**: Desktop app with chat interface
- **Best for**: Non-technical users, quick experiments
- **Limitation**: Less focused on coding pipelines

### GPT4All

- **What**: Desktop app + server, CPU-optimized
- **Best for**: Running on machines without GPU
- **Limitation**: Slower inference, smaller model selection

### LocalAI

- **What**: OpenAI-compatible server (Docker-first)
- **Best for**: Kubernetes/DevOps teams, multiple models
- **Advantage**: Single server, multiple model endpoints
- **Setup**:

```bash
docker run -ti -p 8080:8080 \
  localai/localai:latest-gpu-nvidia-cuda-12 \
  run qwen2.5-coder:32b
```

---

## Decision Matrix

| Tool | Primary Use Case | Installation | Skill Level |
|------|------------------|--------------|:-----------:|
| **Ollama** | CLI dev workflow | One-line | Beginner |
| **LM Studio** | Visual exploration | GUI installer | Beginner |
| **Tabby** | Autocomplete server | Docker | Intermediate |
| **vLLM** | Team/CI server | pip/Docker | Advanced |
| **LocalAI** | K8s deployment | Docker/Helm | Advanced |

---

## Hybrid Setup (Recommended)

For serious development, run multiple tools:

```
Autocomplete:       Tabby + StarCoder2-3B (sub-100ms)
Chat/Refactoring:   Ollama + Qwen2.5-Coder-32B
Team Server:        vLLM (if concurrent users)
Exploration:        LM Studio (model comparison)
```

### Resource Allocation

```bash
# Example: RTX 4090 (24GB VRAM)
# Tabby:  ~4GB (3B model)
# Ollama: ~18GB (32B Q4 model)
# Total:  ~22GB ✓
```

---

## Further Reading

- [Tabby Documentation](https://tabby.tabbyml.com/)
- [LM Studio](https://lmstudio.ai/)
- [LocalAI GitHub](https://github.com/mudler/LocalAI)
- [Jan.ai](https://jan.ai/)

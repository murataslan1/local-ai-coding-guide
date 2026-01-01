# 🔀 Runner Comparison: Ollama vs llama.cpp vs vLLM vs SGLang

> **Which inference engine should you use for local AI coding?**

## Quick Decision Tree

```
Are you a single developer on desktop?
├─ Yes → Do you want simplicity? → Ollama
│       Want fine control? → llama.cpp
│
└─ No → Running a team server?
        ├─ High throughput needed → vLLM
        └─ Structured JSON outputs → SGLang
```

---

## Performance Comparison (Coding Tasks)

| Runner | Throughput (TPS) | Latency (P99) | Best For |
|--------|:----------------:|:-------------:|----------|
| **Ollama** | ~41 | ~673ms | Single dev, easy setup |
| **llama.cpp** | ~44 | ~500ms | CLI hackers, custom builds |
| **vLLM** | **793** | **80ms** | Multi-user servers |
| **SGLang** | **~47** | ~450ms | DeepSeek/Qwen, JSON outputs |

> **Key Insight**: vLLM is **19x faster** than Ollama under concurrent load (Red Hat benchmarks).

---

## Feature Comparison

| Feature | Ollama | llama.cpp | vLLM | SGLang |
|---------|:------:|:---------:|:----:|:------:|
| Easy install | ✅✅✅ | ✅ | ✅✅ | ✅✅ |
| Tool/Function calling | Via client | Via client | ✅ Native | ✅ Native |
| OpenAI API compat | ✅ | ✅ | ✅ | ✅ |
| Long context (128k+) | ✅ | ✅ | ✅✅ | ✅✅ |
| JSON grammar | ❌ | ✅ | ✅ | ✅✅ (xgrammar) |
| Quantization control | Limited | ✅✅ | Limited | Limited |
| Apple Silicon | ✅ | ✅✅ | Limited | Limited |

---

## Detailed Breakdown

### Ollama

**Best for**: Beginners, quick setup, desktop development

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Run
ollama run qwen2.5-coder:32b
```

**Pros**:
- One-line install
- Curated model library
- Works with Continue.dev, Aider out of the box
- Cross-platform

**Cons**:
- Less control over quantization
- Slower under concurrent load
- No native tool calling (client must handle)

---

### llama.cpp

**Best for**: Power users, embedded/edge, maximum control

```bash
# Build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make -j

# Run server
./llama-server -m model.gguf -c 8192 --port 8080
```

**Pros**:
- Fine-grained control (quantization, KV cache, context)
- Works on everything: Pi, phone, Mac, Windows
- OpenAI-compatible server mode
- JSON schema / constrained decoding

**Cons**:
- Requires compilation
- Manual model management
- Steeper learning curve

**What llama.cpp offers that Ollama doesn't**:
- Direct quantization control (Q2–Q8, mix-precision)
- Custom KV cache sizes
- Multiple language bindings (Python, Node.js, Go)
- Embedded/mobile deployment

---

### vLLM

**Best for**: Team servers, multi-user coding agents, CI/CD bots

```bash
# Install
pip install vllm

# Run server
vllm serve Qwen/Qwen2.5-Coder-32B-Instruct --port 8000
```

**Pros**:
- **PagedAttention**: Efficient long-context handling
- **19x faster** than Ollama under concurrent load
- Native tool calling support
- Production-ready for enterprise

**Cons**:
- GPU-only (no CPU fallback)
- Linux-focused
- Higher memory overhead

**Use when**:
- Running OpenDevin, SWE-Agent for a team
- Need API gateway for multiple developers
- Long-context (128k+) codebase analysis

---

### SGLang

**Best for**: DeepSeek/Qwen optimization, structured outputs, research

```bash
# Install
pip install sglang

# Run
sglang serve --model deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct
```

**Pros**:
- **xgrammar**: 10x faster JSON decoding
- Optimized for DeepSeek, Qwen models
- Cache-aware load balancing
- Structured output enforcement

**Cons**:
- Newer, less battle-tested
- Complex setup
- Smaller community

**Use when**:
- Your agents emit structured plans/edits
- Using DeepSeek-Coder or Qwen models
- Need guaranteed JSON schema compliance

---

## Benchmark Data (RTX 4090)

| Model | Ollama | llama.cpp | vLLM | SGLang |
|-------|:------:|:---------:|:----:|:------:|
| DeepSeek R1 8B Q4 | ~68 t/s | ~70 t/s | ~150 t/s | ~155 t/s |
| Qwen2.5-Coder 7B | ~60 t/s | ~65 t/s | ~140 t/s | ~147 t/s |
| Qwen2.5-Coder 32B | ~25 t/s | ~28 t/s | ~60 t/s | ~65 t/s |

> Benchmarks based on single-GPU, batch size 1, 4-bit quantization

---

## Recommendation Matrix

| Your Situation | Use This |
|----------------|----------|
| "I just want it to work" | **Ollama** |
| "I want full control" | **llama.cpp** |
| "I'm running agents for my team" | **vLLM** |
| "I need JSON outputs at scale" | **SGLang** |
| "I'm on Apple Silicon" | **Ollama** or **llama.cpp** |
| "I'm on Windows desktop" | **Ollama** or **LM Studio** |

---

## Further Reading

- [Ollama Documentation](https://docs.ollama.com/)
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [vLLM Documentation](https://docs.vllm.ai/)
- [SGLang Documentation](https://github.com/sgl-project/sglang)
- [Red Hat: Ollama vs vLLM Benchmark](https://developers.redhat.com/articles/2025/08/08/ollama-vs-vllm-deep-dive-performance-benchmarking)

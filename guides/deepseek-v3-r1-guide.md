# DeepSeek V3 + R1: The Complete Local Setup Guide

> **Last Updated**: January 2, 2026

DeepSeek V3 and R1 have effectively closed the gap between open-source and proprietary AI models. This guide covers everything you need to run them locally.

## 🏗️ Architecture Overview

| Specification | DeepSeek V3 | DeepSeek R1 |
|---------------|-------------|-------------|
| **Total Parameters** | 671B | 671B |
| **Active Parameters** | 37B per token | 37B per token |
| **Architecture** | MoE + MLA | MoE + MLA + RL Reasoning |
| **Context Window** | 128K tokens | 128K tokens |
| **Training Cost** | $5.576M | Built on V3 |

### Key Innovations

1. **Multi-head Latent Attention (MLA)**: Compresses KV cache by 40%, enabling 128K context on consumer hardware
2. **DeepSeekMoE**: Fine-grained expert routing for maximum FLOPS efficiency
3. **FP8 Native Training**: 2x speed improvement over FP16

---

## 📊 Benchmarks (January 2026)

| Benchmark | DeepSeek V3 | DeepSeek R1 | Claude 3.5 Sonnet | GPT-4o |
|-----------|-------------|-------------|-------------------|--------|
| HumanEval | 82.6% | 90.2% | 87.3% | 90.2% |
| SWE-bench Verified | 66.0% | 73.1% | 49.0% | ~49% |
| MATH-500 | 85.2% | **97.3%** | 78.3% | 96.4% |
| AIME 2024 | 79.8% | 87.5% | 68.0% | 79.2% |

**Key Insight**: R1 dominates mathematical reasoning; Claude leads in software engineering tasks.

---

## 💻 Hardware Requirements

### Distilled Models (Recommended for Most Users)

| Model | VRAM (Q4) | System RAM | Hardware Example |
|-------|-----------|------------|------------------|
| R1-Distill 1.5B | ~1 GB | 4 GB | Any laptop |
| R1-Distill 7B | ~4 GB | 8 GB | RTX 3060 |
| R1-Distill 14B | ~8 GB | 16 GB | RTX 3080 |
| **R1-Distill 32B** | ~18 GB | 32 GB | **RTX 4090** ⭐ |
| R1-Distill 70B | ~38 GB | 64 GB | Mac Studio M3 |

### Full 671B Model

| Precision | VRAM Required | Recommended Setup |
|-----------|---------------|-------------------|
| FP8 | ~685 GB | 8x H200 141GB |
| INT4 | ~380 GB | Mac Studio Ultra 192GB |

---

## 🚀 Setup Guide

### Option A: Ollama (Easiest)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run distilled models
ollama run deepseek-r1:8b    # 8GB+ RAM (laptop)
ollama run deepseek-r1:32b   # 24GB VRAM (RTX 4090)
ollama run deepseek-r1:70b   # Mac Studio / Multi-GPU
```

### Option B: vLLM (Production)

```bash
pip install vllm

# Single GPU (32B distilled)
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B \
  --quantization fp8 \
  --gpu-memory-utilization 0.95

# Multi-GPU (Full 671B)
vllm serve deepseek-ai/DeepSeek-V3 \
  --tensor-parallel-size 8 \
  --quantization fp8
```

---

## ⚙️ IDE Configuration

### Continue.dev (`~/.continue/config.json`)

```json
{
  "models": [
    {
      "title": "DeepSeek R1 32B (Local)",
      "provider": "ollama",
      "model": "deepseek-r1:32b",
      "apiBase": "http://localhost:11434",
      "contextLength": 128000,
      "completionOptions": {
        "temperature": 0.6
      }
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek V3 1.5B",
    "provider": "ollama",
    "model": "deepseek-r1:1.5b"
  }
}
```

### Cline / Roo Code (OpenAI Compatible)

| Setting | Value |
|---------|-------|
| API Provider | OpenAI Compatible |
| Base URL | `https://api.deepseek.com` |
| Model ID | `deepseek-chat` |
| Context Window | 128000 |

> ⚠️ **Note**: Use `deepseek-chat` for Cline. The `deepseek-reasoner` model's `<think>` tags can confuse XML parsers.

---

## 🎯 When to Use Which Model

| Use Case | Recommended Model |
|----------|-------------------|
| **Fast Autocomplete** | R1-Distill 1.5B (local) |
| **General Coding** | V3 or R1-Distill 32B |
| **Complex Algorithms** | R1 (full or 70B distill) |
| **Multi-file Refactor** | Claude 3.7 Sonnet |
| **Math/Logic Heavy** | R1 (any size) |

---

## 📚 Resources

- [DeepSeek Official Docs](https://deepseek.com)
- [Ollama Model Library](https://ollama.com/library/deepseek-r1)
- [HuggingFace DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1)

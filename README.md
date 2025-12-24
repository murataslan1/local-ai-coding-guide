# 🦙 Local AI Coding Guide

> **Run GPT-4 class AI coding assistants 100% locally. No API costs. No cloud. Total privacy.**

[![Stars](https://img.shields.io/github/stars/murataslan1/local-ai-coding-guide?style=social)](https://github.com/murataslan1/local-ai-coding-guide)
[![Last Updated](https://img.shields.io/badge/Updated-December%202025-brightgreen)](https://github.com/murataslan1/local-ai-coding-guide)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Qwen%202.5%20Coder-32B-orange?style=for-the-badge&logo=alibabacloud"/>
  <img src="https://img.shields.io/badge/Ollama-Ready-success?style=for-the-badge&logo=ollama"/>
  <img src="https://img.shields.io/badge/100%25-Offline-blue?style=for-the-badge"/>
</p>

---

## 📖 Table of Contents

- [Why Local AI?](#-why-local-ai)
- [Quick Start (5 minutes)](#-quick-start)
- [Model Comparison](#-model-comparison)
- [Hardware Requirements](#-hardware-requirements)
- [IDE Integration](#-ide-integration)
- [Optimization Guide](#-optimization-guide)
- [Troubleshooting](#-troubleshooting)
- [Cost Analysis](#-cost-analysis)

---

## 🎯 Why Local AI?

| Cloud AI | Local AI |
|:---------|:---------|
| ❌ $200-500/month API costs | ✅ $0/month after hardware |
| ❌ Your code sent to servers | ✅ 100% private |
| ❌ Network latency | ✅ Instant response |
| ❌ Rate limits | ✅ Unlimited usage |
| ❌ Requires internet | ✅ Works offline |

**2025 Reality:** Open-source models now match GPT-4o in coding tasks. The switch is no longer a compromise—it's an upgrade.

---

## 🚀 Quick Start

### Step 1: Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### Step 2: Download the Best Coding Model

```bash
# For 24GB VRAM (RTX 3090/4090)
ollama pull qwen2.5-coder:32b

# For 16GB VRAM
ollama pull qwen2.5-coder:14b

# For 8GB VRAM or laptops
ollama pull qwen2.5-coder:7b

# For autocomplete (fast, small)
ollama pull qwen2.5-coder:1.5b-base
```

### Step 3: Test It

```bash
ollama run qwen2.5-coder:32b
>>> Write a Python function to find prime numbers
```

### Step 4: Install Continue.dev (VS Code)

1. Install [Continue extension](https://marketplace.visualstudio.com/items?itemName=Continue.continue)
2. Open settings: `~/.continue/config.json`
3. Configure:

```json
{
  "models": [
    {
      "title": "Qwen 2.5 Coder 32B",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen 1.5B (Fast)",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b-base"
  }
}
```

**Done!** You now have a local Copilot alternative.

---

## 📊 Model Comparison

### Best Models for Local Coding (December 2025)

| Model | Size | VRAM | HumanEval | Best For |
|:------|:-----|:-----|:----------|:---------|
| **Qwen 2.5 Coder 32B** 👑 | 32B | 24GB | 92.7% | The KING. Best all-around. |
| DeepSeek V3 | 671B | 200GB+ | 89.0% | Frontier. Multi-GPU only. |
| DeepSeek R1-Distill-32B | 32B | 24GB | ~90% | Reasoning + coding hybrid |
| Qwen 2.5 Coder 14B | 14B | 16GB | ~85% | Mid-range GPUs |
| Qwen 2.5 Coder 7B | 7B | 8GB | ~80% | Laptops, fast autocomplete |
| Codestral 22B | 22B | 20GB | ~82% | FIM specialist |
| Llama 3.3 70B | 70B | 48GB | 87.6% | General + coding |

### Architecture Note

- **Dense (Qwen, Llama):** Predictable VRAM usage. Simple deployment.
- **MoE (DeepSeek V3):** More parameters, fewer active. Complex but efficient.

---

## 💻 Hardware Requirements

### VRAM Requirements (4-bit Quantization)

| Model Size | Minimum | Recommended | GPU Examples |
|:-----------|:--------|:------------|:-------------|
| **7B** | 6 GB | 8 GB | RTX 3060, M1/M2/M3 8GB |
| **14B** | 10 GB | 16 GB | RTX 4060 Ti 16GB |
| **32B** | 18 GB | 24 GB | RTX 3090/4090, M-series 32GB+ |
| **70B** | 40 GB | 48 GB | 2x 3090, Mac Studio 64GB |

### NVIDIA GPUs (Speed King)

| GPU | VRAM | Best Model | Speed |
|:----|:-----|:-----------|:------|
| RTX 3060 12GB | 12GB | Qwen 14B | ~30 t/s |
| RTX 3080 10GB | 10GB | Qwen 7B | ~50 t/s |
| **RTX 3090** | **24GB** | **Qwen 32B** | **~50 t/s** |
| **RTX 4090** | **24GB** | **Qwen 32B** | **~100 t/s** |
| 2x RTX 3090 | 48GB | Llama 70B | ~20 t/s |

### Apple Silicon (Capacity King)

| Mac | RAM | Best Model | Speed |
|:----|:----|:-----------|:------|
| M1/M2 8GB | 8GB | Qwen 7B | ~15 t/s |
| M2 Pro 16GB | 16GB | Qwen 14B | ~20 t/s |
| M3 Max 36GB | 36GB | Qwen 32B | ~20 t/s |
| M3 Max 128GB | 128GB | Llama 70B | ~10 t/s |
| Mac Studio 192GB | 192GB | DeepSeek V3 | ~5 t/s |

> **Tip:** Apple Silicon is slower but can run HUGE models due to unified memory.

---

## 🔧 IDE Integration

### Continue.dev (Recommended)

Works with: **VS Code**, **JetBrains**, **Cursor**

```json
// ~/.continue/config.json
{
  "models": [
    {
      "title": "Qwen 32B (Chat)",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen 1.5B (Autocomplete)",
    "provider": "ollama", 
    "model": "qwen2.5-coder:1.5b-base"
  }
}
```

### Cursor (Local Mode)

1. Settings → Models → OpenAI API Base URL
2. Set to: `http://localhost:11434/v1`
3. API Key: `ollama` (any string works)
4. Select model: `qwen2.5-coder:32b`

### Neovim (avante.nvim)

```lua
-- lua/plugins/avante.lua
require("avante").setup({
  provider = "ollama",
  ollama = {
    model = "qwen2.5-coder:32b",
  }
})
```

---

## ⚡ Optimization Guide

### Increase Context Window

```bash
# Create custom model with 32k context
cat << 'EOF' > Modelfile
FROM qwen2.5-coder:32b
PARAMETER num_ctx 32768
SYSTEM "You are an expert coding assistant."
EOF

ollama create qwen32k -f Modelfile
ollama run qwen32k
```

### Keep Model in Memory

```bash
# Prevent model unloading (default: 5 min timeout)
export OLLAMA_KEEP_ALIVE=-1
```

### Quantization Levels

| Level | Size Reduction | Quality | Use Case |
|:------|:---------------|:--------|:---------|
| **Q4_K_M** | ~75% | ⭐⭐⭐⭐ | **Default. Best balance.** |
| Q5_K_M | ~70% | ⭐⭐⭐⭐⭐ | Premium quality |
| Q8_0 | ~50% | ⭐⭐⭐⭐⭐ | If VRAM allows |
| Q2_K | ~85% | ⭐⭐ | Avoid for coding |

> **Warning:** Don't go below Q4 for coding. Logic breaks at low precision.

---

## 🐛 Troubleshooting

### Out of Memory (OOM)

```bash
# Check what's loaded
ollama ps

# Reduce context window
ollama run qwen2.5-coder:32b --ctx 8192

# Try smaller model
ollama run qwen2.5-coder:14b
```

### Slow Inference

1. Check GPU offloading: `nvidia-smi` or `ollama ps`
2. Ensure full GPU load (not CPU fallback)
3. Close other GPU-heavy apps
4. Use smaller model for faster response

### Model Not Following Instructions

- Use **Instruct** models for chat (e.g., `qwen2.5-coder:32b`)
- Use **Base** models for autocomplete (e.g., `qwen2.5-coder:1.5b-base`)
- Add system prompt in Modelfile

### Mac VRAM Expansion (Advanced)

```bash
# Allocate more unified memory to GPU
sudo sysctl iogpu.wired_limit_mb=32000
```

---

## 💰 Cost Analysis

### API vs Local Comparison

| Factor | OpenAI GPT-4o | Local (RTX 3090) |
|:-------|:--------------|:-----------------|
| Monthly API Cost | $200-500 | $0 |
| Hardware Cost | $0 | ~$800 (used) |
| Break-even | - | **2-4 months** |
| Electricity | $0 | ~$10/month |
| Privacy | ❌ Code sent to cloud | ✅ 100% local |

### ROI Calculator

```
Monthly API Usage: $300
RTX 3090 Cost: $800
Break-even: 800 / 300 = 2.7 months

After 1 year savings: $3,600 - $800 - $120 = $2,680
```

> **Insight:** If you already have a gaming PC or MacBook, local AI is essentially **free**.

---

## 🔗 Resources

- [Ollama Documentation](https://docs.ollama.com/)
- [Continue.dev Docs](https://docs.continue.dev/)
- [Qwen 2.5 Coder on HuggingFace](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA) - Best community
- [LM Studio](https://lmstudio.ai/) - GUI alternative

---

## 🤝 Contributing

PRs welcome! Help us keep this guide updated as new models and tools are released.

1. Fork this repo
2. Add your changes
3. Submit a PR

---

## 📜 License

MIT License - Use freely, contribute back!

---

<p align="center">
  <b>⭐ Star this repo if it helped you!</b>
  <br><br>
  Made with ❤️ by <a href="https://github.com/murataslan1">Murat Aslan</a>
  <br>
  Last updated: December 2025
</p>

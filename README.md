<div align="center">

<img src="assets/banner.png" alt="Local AI Coding Guide Banner" width="100%">

# 🦙 Local AI Coding Guide

**Run GPT-4 class AI coding assistants 100% locally. No API costs. No cloud. Total privacy.**

[![GitHub stars](https://img.shields.io/github/stars/murataslan1/local-ai-coding-guide?style=for-the-badge&logo=github&color=yellow)](https://github.com/murataslan1/local-ai-coding-guide/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/murataslan1/local-ai-coding-guide?style=for-the-badge&logo=github&color=blue)](https://github.com/murataslan1/local-ai-coding-guide/network/members)
[![Last Updated](https://img.shields.io/badge/Updated-January%202026-brightgreen?style=for-the-badge)](https://github.com/murataslan1/local-ai-coding-guide)

[![Qwen](https://img.shields.io/badge/Qwen%202.5%20Coder-32B-orange?style=for-the-badge&logo=alibabacloud)](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)
[![Ollama](https://img.shields.io/badge/Ollama-Ready-success?style=for-the-badge)](https://ollama.com)
[![Privacy](https://img.shields.io/badge/100%25-Offline-blue?style=for-the-badge)](https://github.com/murataslan1/local-ai-coding-guide)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Complete guide with agentic workflows, prompt engineering, runner comparison, and real-world examples*

<br>

**⚡ Quick Links:**

[🚀 Quick Start](#-quick-start) · [🤖 Agentic Coding](#-agentic-coding-new) · [🔀 Runners](#-runner-comparison) · [🛡️ Guardrails](#️-guardrails--coding-plans) · [🎯 Prompts](#-prompt-engineering) · [🗣️ Community](#-community-experiences) · [⚠️ Gotchas](#️-gotchas)

</div>

---

## 📋 Table of Contents

<details>
<summary><b>Click to expand full navigation</b></summary>

### 🚀 Getting Started
- [Why Local AI?](#-why-local-ai)
- [Quick Start (5 min)](#-quick-start)
- [Hardware Requirements](#-hardware-requirements)

### 🔧 Infrastructure
- [Runner Comparison](#-runner-comparison) - Ollama vs llama.cpp vs vLLM
- [Model Selection](#-model-comparison)
- [IDE Integration](#-ide-integration)
- [Alternative Tools](#-alternative-tools) - LM Studio, Tabby

### 🤖 Advanced Workflows (NEW)
- [Agentic Coding](#-agentic-coding-new) - Autonomous bug fixing
- [Guardrails & TDD](#️-guardrails--coding-plans) - Prevent hallucinations
- [Prompt Engineering](#-prompt-engineering) - Better local prompts
- [Real-World Workflows](#-real-world-workflows)
- [Community Experiences](#-community-experiences) - Reddit/HN insights
- [Advanced Patterns](#-advanced-patterns) - Architect-Builder, YOLO Mode

### ⚠️ Troubleshooting
- [FAQ](#-faq) - Quick answers
- [Gotchas & Common Mistakes](#️-gotchas)
- [Diagrams](#-diagrams) - Visual workflows
- [Optimization Guide](#-optimization-guide)
- [Cost Analysis](#-cost-analysis)

### 🛠️ Tools & Configs
- [Docker Compose](#-docker-compose) - One-command setup
- [Config Templates](#-config-templates) - Ready-to-use configs
- [Benchmark Script](#-benchmark-script) - Test your hardware

</details>

---

## 🎯 Why Local AI?

| Cloud AI | Local AI |
|:---------|:---------:|
| ❌ $200-500/month API costs | ✅ **$0/month** after hardware |
| ❌ Your code sent to servers | ✅ **100% private** |
| ❌ Network latency (~200-500ms) | ✅ **<50ms** response |
| ❌ Rate limits | ✅ **Unlimited** usage |
| ❌ Requires internet | ✅ **Works offline** |

> **2026 Reality**: Qwen2.5-Coder-32B scores **92.7% on HumanEval**, matching GPT-4o. The switch is no longer a compromise—it's an upgrade.

### The Bandwidth Formula

```
Speed (t/s) ≈ Memory Bandwidth (GB/s) / Model Size (GB)

Example: RTX 4090 (1008 GB/s) + Qwen 32B Q4 (18GB)
         ≈ 1008 / 18 = 56 t/s ✓
```

---

## 🚀 Quick Start

### Step 1: Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows - Download from https://ollama.com/download
```

### Step 2: Download Coding Model

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
2. Configure `~/.continue/config.json`:

```json
{
  "models": [{
    "title": "Qwen 32B (Chat)",
    "provider": "ollama",
    "model": "qwen2.5-coder:32b"
  }],
  "tabAutocompleteModel": {
    "title": "Qwen 1.5B (Fast)",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b-base"
  }
}
```

**Done!** You now have a local Copilot alternative.

---

## 🔀 Runner Comparison

> **vLLM is 19x faster than Ollama** under concurrent load (Red Hat benchmarks).

| Runner | Throughput | Best For |
|--------|:----------:|----------|
| **Ollama** | ~41 TPS | Single dev, easy setup |
| **llama.cpp** | ~44 TPS | CLI hackers, full control |
| **vLLM** | **~793 TPS** | Team servers, CI/CD |
| **SGLang** | ~47 TPS | DeepSeek, structured JSON |

### Quick Decision

```
Single developer on desktop?
├─ Want simplicity? → Ollama
└─ Want control? → llama.cpp

Running team server?
├─ High throughput? → vLLM
└─ JSON outputs? → SGLang
```

📖 **[Full Runner Comparison Guide →](guides/runner-comparison.md)**

---

## 🤖 Agentic Coding (NEW!)

> **Reddit's #1 requested feature**: "Show me a real workflow, not just setup."

### The Bug Fix Workflow (Aider + Ollama)

```bash
# Install Aider
pip install aider-chat

# Configure for Ollama
cat > ~/.aider.conf.yml << 'EOF'
model: ollama/qwen2.5-coder:32b
openai-api-base: http://localhost:11434/v1
openai-api-key: "ollama"
EOF

# Start fixing bugs!
cd /your/project
aider .
```

### Example Session

```
YOU: Tests test_user_login and test_user_logout are failing. Please:
     1) Run `pytest tests/test_auth.py`
     2) Read failing tests and source files
     3) Explain the bug and create a plan
     4) Apply minimal fix
     5) Run tests until they pass

AIDER: [Reads files, proposes fix, applies, runs tests, iterates...]

YOU: git diff  # Review
YOU: git commit -am "Fix auth bug"
```

### Continue.dev Agent Mode

1. Open failing file in VS Code
2. Open Continue → Select **Agent mode**
3. Prompt with specific instructions
4. Let Agent iterate with tools

📖 **[Full Agentic Coding Guide →](guides/agentic-coding.md)**

---

## 🛡️ Guardrails & Coding Plans

> **Prevent local models from hallucinating and breaking your code.**

### Strategy 1: TDD as Feedback Loop

```
1. YOU write failing test
2. AI implements code
3. Test runs automatically
4. If fail → AI analyzes, retries
5. If pass → Move to next feature
```

### Strategy 2: Plan Before Code

```
PROMPT (Step 1 - Plan):
"Analyze the failing test. DO NOT write code yet.
Create a numbered plan with 3-7 steps."

PROMPT (Step 2 - Execute):
"I approve the plan. Now implement step by step.
Run tests after each major change."
```

### Strategy 3: Scope Limiting

```
RULES:
- Only modify: PaymentService.ts
- Do NOT touch: config.ts, package.json
- Do NOT add new files
```

📖 **[Full Guardrails Guide →](guides/guardrails.md)**

---

## 🎯 Prompt Engineering

> **Local models need better prompts than GPT-4.**

### The CO-STAR Framework

```
CONTEXT: You are editing a TypeScript monorepo with Next.js.
OBJECTIVE: Fix the failing tests without breaking other components.
STYLE: Clear, idiomatic TypeScript; minimal changes.
RESPONSE: 
  1. Short explanation (3-5 bullets)
  2. Step-by-step plan
  3. Unified diff for changed files only
```

### Identity Reinforcement

```
"You are Qwen, a highly capable coding assistant created by Alibaba Cloud.
You are an expert in algorithms, system design, and clean code principles.
You strictly adhere to user constraints and always think step-by-step."
```

### System Prompt Template

```
You are a coding assistant focused on small, safe changes.

RULES:
1. Never invent external APIs
2. Prefer minimal diffs over rewrites
3. Keep style consistent with existing code
4. If ambiguous, ask clarifying questions
5. Output ONLY unified diffs
```

📖 **[Full Prompt Engineering Guide →](guides/prompt-engineering.md)**

---

## 📊 Model Comparison

| Model | Size | VRAM | HumanEval | Best For |
|:------|:-----|:-----|:----------|:---------:|
| **Qwen 2.5 Coder 32B** 👑 | 32B | 24GB | **92.7%** | All-around KING |
| DeepSeek-Coder-V2 | 236B (MoE) | 48GB+ | ~89% | Multi-GPU setups |
| Qwen 2.5 Coder 14B | 14B | 16GB | ~85% | Mid-range GPUs |
| Qwen 2.5 Coder 7B | 7B | 8GB | ~80% | Laptops |
| Codestral 22B | 22B | 20GB | ~82% | FIM specialist |

### Quantization Guidance

| Quant | Quality | Use Case |
|:------|:-------:|:---------|
| **Q4_K_M** | ⭐⭐⭐⭐ | **Default. Best balance.** |
| Q5_K_M | ⭐⭐⭐⭐⭐ | Complex refactors |
| Q8_0 | ⭐⭐⭐⭐⭐ | If VRAM allows |
| Q2_K | ⭐⭐ | ❌ **Avoid for coding** |

> **Warning**: Don't go below Q4 for coding. Logic breaks at low precision.

---

## 💻 Hardware Requirements

### The Speed Formula

```
Speed (t/s) ≈ Memory Bandwidth (GB/s) / Model Size (GB)
```

| Hardware | Bandwidth | 32B Q4 Speed |
|----------|:---------:|:------------:|
| RTX 4090 (24GB) | 1008 GB/s | ~56 t/s |
| RTX 3090 (24GB) | 936 GB/s | ~52 t/s |
| M3 Max (96GB) | 400 GB/s | ~22 t/s |
| RTX 4060 Ti (16GB) | 288 GB/s | N/A (won't fit) |

### Recommendations

| Persona | Hardware | Best Model | Speed |
|---------|----------|------------|:-----:|
| **Budget Learner** | RTX 3060 12GB | Qwen 7B | ~40 t/s |
| **Pro Developer** | RTX 4090 24GB | Qwen 32B | ~56 t/s |
| **AI Architect** | Mac Studio 128GB | Llama 70B | ~22 t/s |
| **Home Lab** | Dual RTX 3090 | Llama 70B Q5 | ~35 t/s |

---

## 🔧 IDE Integration

### Continue.dev (Recommended)

```json
{
  "models": [{
    "title": "Qwen 32B",
    "provider": "ollama",
    "model": "qwen2.5-coder:32b"
  }],
  "tabAutocompleteModel": {
    "title": "StarCoder2 3B",
    "provider": "ollama",
    "model": "starcoder2:3b"
  }
}
```

### Cursor (Local Mode)

```
Settings → Models → OpenAI API Base URL
→ http://localhost:11434/v1
API Key: ollama
Model: qwen2.5-coder:32b
```

### Aider (Terminal)

```bash
pip install aider-chat
export OLLAMA_API_BASE=http://localhost:11434
aider --model ollama/qwen2.5-coder:32b
```

---

## 🖥️ Alternative Tools

| Tool | Best For |
|------|----------|
| **[LM Studio](https://lmstudio.ai)** | Visual exploration, model comparison |
| **[Tabby](https://tabby.tabbyml.com)** | Self-hosted autocomplete (<100ms) |
| **[LocalAI](https://github.com/mudler/LocalAI)** | Kubernetes/DevOps, multi-model |
| **[vLLM](https://docs.vllm.ai)** | Team servers, CI/CD pipelines |

📖 **[Full Alternative Tools Guide →](guides/alternative-tools.md)**

---

## 🔄 Real-World Workflows

### Workflow 1: Debug React Component

```
1. Open failing file + test in VS Code
2. Continue Agent mode
3. Prompt: "Avatar doesn't update after profile change..."
4. Let agent read, test, fix, iterate
5. Review diffs and commit
```

### Workflow 2: Add API Endpoint (TDD)

```
1. Write failing test first
2. Aider: "Implement /api/users/{id} to pass the test"
3. Agent implements, runs tests, iterates
4. Review and commit
```

### Workflow 3: Refactor Legacy Code

```
1. Plan mode: "Create characterization tests"
2. Agent mode: "Refactor to Python 3.12"
3. Verify all tests pass
4. Review and commit
```

📖 **[Full Workflows Guide →](guides/workflows.md)**

---

## ⚠️ Gotchas

### Top 5 Mistakes

| Mistake | Fix |
|---------|-----|
| **Expecting GPT-4 from 7B** | Use 32B for complex tasks |
| **Dumping entire repo** | Limit to relevant files |
| **Using Q2 quantization** | Stay ≥Q4 for coding |
| **Long sessions** | Clear context regularly |
| **No tests** | Always have verification |

### Context Window Exhaustion

```
Symptoms:
- Model repeats itself
- Ignores instructions
- Quality drops suddenly

Fix:
- /clear or restart session
- Use RAG instead of stuffing
- Summarize before continuing
```

📖 **[Full Gotchas Guide →](guides/gotchas.md)**

---

## ⚡ Optimization Guide

### Keep Model in Memory

```bash
export OLLAMA_KEEP_ALIVE=-1  # Never unload
```

### Increase Context Window

```bash
cat << 'EOF' > Modelfile
FROM qwen2.5-coder:32b
PARAMETER num_ctx 32768
EOF
ollama create qwen32k -f Modelfile
```

---

## 💰 Cost Analysis

| Factor | Cloud (GPT-4o) | Local (RTX 4090) |
|--------|:--------------:|:----------------:|
| Monthly Cost | $200-500 | **$0** |
| Hardware | $0 | ~$1,800 one-time |
| Break-even | - | **4-9 months** |
| Privacy | ❌ | ✅ |
| Offline | ❌ | ✅ |

> **Insight**: If you already have a gaming PC, local AI is essentially **free**.

---

## 📈 Star History

<a href="https://star-history.com/#murataslan1/local-ai-coding-guide&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=murataslan1/local-ai-coding-guide&type=Date&theme=dark" />
   <img alt="Star History" src="https://api.star-history.com/svg?repos=murataslan1/local-ai-coding-guide&type=Date" />
 </picture>
</a>

---

## 📚 Resources

| Resource | Link |
|----------|------|
| 📖 Ollama Docs | [docs.ollama.com](https://docs.ollama.com) |
| 🔧 Continue.dev | [docs.continue.dev](https://docs.continue.dev) |
| 🤖 Aider | [aider.chat](https://aider.chat) |
| 🦙 r/LocalLLaMA | [reddit.com/r/LocalLLaMA](https://reddit.com/r/LocalLLaMA) |
| 🏷️ Qwen2.5-Coder | [Hugging Face](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct) |

---

## 🤝 Contributing

<div align="center">

[![Contributors](https://contrib.rocks/image?repo=murataslan1/local-ai-coding-guide)](https://github.com/murataslan1/local-ai-coding-guide/graphs/contributors)

</div>

We welcome contributions! Help us keep this guide updated.

| Type | Examples |
|------|----------|
| 🆕 Tips | Workflows, shortcuts, hidden features |
| 🐛 Bug Reports | New issues, workarounds |
| 📊 Benchmarks | Model comparisons, speed tests |
| 🔧 Configs | Modelfiles, Continue configs |

1. Fork this repo
2. Add your changes
3. Submit a PR

---

## 💝 Support

<div align="center">

[![Star](https://img.shields.io/badge/⭐_Star_This_Repo-yellow?style=for-the-badge)](https://github.com/murataslan1/local-ai-coding-guide)
[![Share Twitter](https://img.shields.io/badge/Share_on_Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/intent/tweet?text=Check%20out%20this%20local%20AI%20coding%20guide!&url=https://github.com/murataslan1/local-ai-coding-guide)

**⭐ Star this repo if it helped you!**

Made with ❤️ by [Murat Aslan](https://github.com/murataslan1)

[![Follow](https://img.shields.io/github/followers/murataslan1?label=Follow&style=social)](https://github.com/murataslan1)

*Last updated: January 2026*

</div>

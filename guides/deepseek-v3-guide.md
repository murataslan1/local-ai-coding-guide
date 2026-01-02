# DeepSeek V3 and R1: The Open-Weights Revolution

> **Status**: Verified for Jan 2026
> **Focus**: Local Inference, Reasoning, Distillation

## 1. Overview
The release of DeepSeek-V3 and its reasoning-specialized variable, DeepSeek-R1, marks the end of the "Capability Gap" between closed-source API models (GPT-4o) and local open-weights models. For the first time, developers can run a "System 2" reasoning engine entirely offline on consumer hardware.

---

## 2. DeepSeek-V3: Architecture
DeepSeek-V3 is a massive Mixture-of-Experts (MoE) model.
- **Total Parameters**: 671B
- **Active Parameters**: 37B (per token)
- **Context Length**: 128k Tokens

### Key Innovations
1.  **Multi-head Latent Attention (MLA)**:
    *   Compresses Key-Value (KV) cache into a low-dimensional latent space.
    *   Drastically reduces VRAM usage for long contexts.
    *   Enables 128k context on single GPUs where other 70B+ models fail.

2.  **DeepSeekMoE**:
    *   Uses fine-grained expert segmentation to ensure maximum FLOPS efficiency.
    *   Load balancing ensures no "dead experts".

---

## 3. DeepSeek-R1: "System 2" Reasoning
DeepSeek-R1 introduces **Chain-of-Thought (CoT)** reasoning trained via pure Reinforcement Learning (RL), without massive Supervised Fine-Tuning (SFT).

*   **Behavior**: The model generates internal monologues (marked by `<think>` tags) to break down complex coding or math problems.
*   **Performance**: Achieves **97.3% on MATH-500**, surpassing GPT-4o.
*   **Self-Correction**: It can backtrack, verify assumptions, and fix its own logic before outputting code.

### Distillation: The Local Sweet Spot
DeepSeek distilled R1's reasoning capabilities into smaller, dense architectures (Qwen-2.5 and Llama-3).

| Model | Params | Use Case | VRAM Req (4-bit) |
| :--- | :--- | :--- | :--- |
| **R1-Distill-Qwen-1.5B** | 1.5B | Edge / IoT | 2GB |
| **R1-Distill-Qwen-7B** | 7B | Copilot / Autocomplete | 6GB |
| **R1-Distill-Qwen-14B** | 14B | Advanced Assistant | 10GB |
| **R1-Distill-Qwen-32B** | 32B | **Local Expert (Sweet Spot)** | 22GB |
| **R1-Distill-Llama-70B** | 70B | Research Node | 40GB |

> [!TIP]
> **R1-Distill-Qwen-32B** is widely considered the best local coding model as of Jan 2026. It outperforms GPT-4o on some benchmarks while fitting on a single RTX 3090/4090.

---

## 4. Hardware Requirements
Local AI in 2026 is limited by **Memory Bandwidth**, not Compute (FLOPS).

### The "RAM Crisis"
*   **VRAM (GPU Memory)**: The gold standard (>1,000 GB/s).
*   **System RAM**: The bottleneck (~100 GB/s).
*   **Rule**: If the model doesn't fit in VRAM, performance drops from 50 t/s to 1 t/s.

### Recommended Setups
1.  **The Enthusiast**: **NVIDIA RTX 3090 / 4090 (24GB VRAM)**.
    *   Perfect for R1-Distill-Qwen-32B (4-bit).
    *   ~50 tokens/sec.
2.  **The Workstation**: **Mac Studio (M2/M3/M4 Ultra) with 192GB Unified Memory**.
    *   Can run the full **DeepSeek-R1 (671B)** quantized.
    *   ~10-15 tokens/sec.
3.  **The Budget**: **RTX 3060 (12GB VRAM)**.
    *   Runs R1-Distill-Qwen-14B or 7B comfortably.

---

## 5. Quick Start (Ollama)
Run the distilled models locally using Ollama.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh

# Run the 7B model (Fast, good for autocomplete)
ollama run deepseek-r1:7b

# Run the 32B model (The Specialist - Requires 24GB VRAM)
ollama run deepseek-r1:32b
```

## 6. Optimization Tools
*   **Unsloth**: Use Unsloth-optimized GGUF builds for dynamic quantization (e.g., 1.58-bit layers) to fit larger models into smaller VRAM.
*   **llama.cpp**: Use for manual shard loading if you have a split CPU/GPU setup.

#!/usr/bin/env python3
"""
Local AI Benchmark Script
=========================
Test your hardware's performance with local LLMs.

Usage:
    python benchmark.py
    python benchmark.py --model qwen2.5-coder:32b
    python benchmark.py --all

Requirements:
    pip install requests rich
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime

try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "rich"])
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel

console = Console()

# Benchmark prompts
PROMPTS = {
    "simple": "Write a Python function to check if a number is prime. Output only the code.",
    "medium": """Write a Python class called UserService that:
1. Has methods for create_user, get_user, delete_user
2. Uses a dictionary as in-memory storage
3. Includes proper type hints
4. Has docstrings for each method
Output only the code.""",
    "complex": """Write a complete FastAPI REST API with:
1. User model with id, name, email fields
2. CRUD endpoints (GET, POST, PUT, DELETE)
3. Proper error handling with HTTPException
4. Input validation using Pydantic
5. Include all necessary imports
Output only the code."""
}


def get_system_info():
    """Get system hardware information."""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu": platform.processor() or "Unknown",
        "python": platform.python_version(),
    }
    
    # Get RAM
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True
            )
            ram_bytes = int(result.stdout.strip())
            info["ram_gb"] = ram_bytes / (1024**3)
        else:  # Linux
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        ram_kb = int(line.split()[1])
                        info["ram_gb"] = ram_kb / (1024**2)
                        break
    except:
        info["ram_gb"] = "Unknown"
    
    # Check for GPU
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            info["gpu"] = result.stdout.strip()
        else:
            info["gpu"] = "No NVIDIA GPU detected"
    except:
        if platform.system() == "Darwin":
            info["gpu"] = "Apple Silicon (Metal)"
        else:
            info["gpu"] = "No GPU detected"
    
    return info


def check_ollama():
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_available_models():
    """Get list of available models in Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        data = response.json()
        return [model["name"] for model in data.get("models", [])]
    except:
        return []


def benchmark_model(model_name: str, prompt_type: str = "medium"):
    """Run benchmark on a specific model."""
    prompt = PROMPTS.get(prompt_type, PROMPTS["medium"])
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024
        }
    }
    
    start_time = time.time()
    first_token_time = None
    
    try:
        # Non-streaming request for simplicity
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=300
        )
        end_time = time.time()
        
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}
        
        data = response.json()
        
        total_time = end_time - start_time
        eval_count = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 1)
        prompt_eval_duration_ns = data.get("prompt_eval_duration", 1)
        
        # Calculate metrics
        tokens_per_second = eval_count / (eval_duration_ns / 1e9) if eval_duration_ns > 0 else 0
        ttft = prompt_eval_duration_ns / 1e9  # Time to first token
        
        return {
            "model": model_name,
            "prompt_type": prompt_type,
            "total_time": round(total_time, 2),
            "tokens_generated": eval_count,
            "tokens_per_second": round(tokens_per_second, 2),
            "ttft": round(ttft, 3),
            "output_length": len(data.get("response", "")),
            "success": True
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out (>300s)"}
    except Exception as e:
        return {"error": str(e)}


def run_benchmarks(models: list, prompt_types: list = None):
    """Run benchmarks on specified models."""
    if prompt_types is None:
        prompt_types = ["simple", "medium", "complex"]
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for model in models:
            for prompt_type in prompt_types:
                task = progress.add_task(
                    f"Testing {model} ({prompt_type})...",
                    total=None
                )
                
                result = benchmark_model(model, prompt_type)
                results.append(result)
                
                progress.remove_task(task)
    
    return results


def display_results(results: list, system_info: dict):
    """Display benchmark results in a nice table."""
    
    # System info panel
    sys_text = f"""
**OS**: {system_info['os']} {system_info.get('os_version', '')[:30]}
**CPU**: {system_info.get('cpu', 'Unknown')[:40]}
**RAM**: {system_info.get('ram_gb', 'Unknown'):.1f} GB
**GPU**: {system_info.get('gpu', 'Unknown')}
"""
    console.print(Panel(sys_text, title="🖥️ System Information", border_style="blue"))
    
    # Results table
    table = Table(title="📊 Benchmark Results", show_header=True, header_style="bold cyan")
    table.add_column("Model", style="dim")
    table.add_column("Prompt", style="dim")
    table.add_column("Tokens/sec", justify="right")
    table.add_column("TTFT (s)", justify="right")
    table.add_column("Total (s)", justify="right")
    table.add_column("Tokens", justify="right")
    
    for r in results:
        if "error" in r:
            table.add_row(
                r.get("model", "?"),
                r.get("prompt_type", "?"),
                f"[red]Error[/red]",
                "-",
                "-",
                "-"
            )
        else:
            # Color code tokens/sec
            tps = r["tokens_per_second"]
            if tps >= 40:
                tps_str = f"[green]{tps}[/green]"
            elif tps >= 20:
                tps_str = f"[yellow]{tps}[/yellow]"
            else:
                tps_str = f"[red]{tps}[/red]"
            
            table.add_row(
                r["model"],
                r["prompt_type"],
                tps_str,
                str(r["ttft"]),
                str(r["total_time"]),
                str(r["tokens_generated"])
            )
    
    console.print(table)
    
    # Summary
    successful = [r for r in results if r.get("success")]
    if successful:
        avg_tps = sum(r["tokens_per_second"] for r in successful) / len(successful)
        console.print(f"\n[bold green]Average Tokens/sec:[/bold green] {avg_tps:.2f}")
        
        # Recommendations
        console.print("\n[bold]💡 Recommendations:[/bold]")
        if avg_tps >= 40:
            console.print("[green]✅ Excellent performance! Your setup is production-ready.[/green]")
        elif avg_tps >= 20:
            console.print("[yellow]⚠️ Good performance. Consider Q8 quant or smaller model for better speed.[/yellow]")
        else:
            console.print("[red]❌ Slow performance. Try smaller model, higher quant, or check GPU utilization.[/red]")


def save_results(results: list, system_info: dict):
    """Save results to JSON file."""
    output = {
        "timestamp": datetime.now().isoformat(),
        "system": system_info,
        "results": results
    }
    
    filename = f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    
    console.print(f"\n[dim]Results saved to {filename}[/dim]")


def main():
    parser = argparse.ArgumentParser(description="Benchmark local LLM performance")
    parser.add_argument("--model", "-m", help="Specific model to test")
    parser.add_argument("--all", "-a", action="store_true", help="Test all available models")
    parser.add_argument("--save", "-s", action="store_true", help="Save results to JSON")
    args = parser.parse_args()
    
    console.print(Panel.fit(
        "[bold blue]🦙 Local AI Benchmark Tool[/bold blue]\n"
        "Testing your hardware's LLM performance",
        border_style="blue"
    ))
    
    # Check Ollama
    if not check_ollama():
        console.print("[red]❌ Ollama is not running![/red]")
        console.print("Start Ollama with: [cyan]ollama serve[/cyan]")
        sys.exit(1)
    
    console.print("[green]✅ Ollama is running[/green]\n")
    
    # Get system info
    system_info = get_system_info()
    
    # Determine models to test
    available = get_available_models()
    if not available:
        console.print("[red]No models found![/red]")
        console.print("Pull a model with: [cyan]ollama pull qwen2.5-coder:7b[/cyan]")
        sys.exit(1)
    
    if args.model:
        if args.model in available:
            models = [args.model]
        else:
            console.print(f"[red]Model '{args.model}' not found![/red]")
            console.print(f"Available: {', '.join(available)}")
            sys.exit(1)
    elif args.all:
        models = available
    else:
        # Default: test first available model
        models = [available[0]]
        console.print(f"Testing model: [cyan]{models[0]}[/cyan]")
        console.print(f"[dim]Use --all to test all {len(available)} available models[/dim]\n")
    
    # Run benchmarks
    results = run_benchmarks(models)
    
    # Display results
    display_results(results, system_info)
    
    # Save if requested
    if args.save:
        save_results(results, system_info)


if __name__ == "__main__":
    main()

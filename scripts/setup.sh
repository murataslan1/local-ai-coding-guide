#!/bin/bash

# =====================================================
# Local AI Coding Setup Script
# One-command setup for local AI development environment
# =====================================================
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/murataslan1/local-ai-coding-guide/main/scripts/setup.sh | bash
#
# Or download and run:
#   chmod +x setup.sh && ./setup.sh
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ASCII Art Banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║        🦙 Local AI Coding Guide - Setup Script 🦙        ║"
    echo "╠══════════════════════════════════════════════════════════╣"
    echo "║  Ollama + Qwen2.5-Coder + Continue.dev                   ║"
    echo "║  100% Local • 100% Private • $0/month                    ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="linux";;
        Darwin*)    OS="macos";;
        CYGWIN*|MINGW*|MSYS*) OS="windows";;
        *)          OS="unknown";;
    esac
    log_info "Detected OS: $OS"
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check RAM
    if [ "$OS" = "macos" ]; then
        TOTAL_RAM=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
    else
        TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    fi
    
    if [ "$TOTAL_RAM" -lt 16 ]; then
        log_warning "You have ${TOTAL_RAM}GB RAM. Recommended: 16GB+ for 7B models, 32GB+ for 32B models."
    else
        log_success "RAM: ${TOTAL_RAM}GB ✓"
    fi
    
    # Check for NVIDIA GPU
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "")
        if [ -n "$GPU_INFO" ]; then
            log_success "NVIDIA GPU detected: $GPU_INFO"
        fi
    elif [ "$OS" = "macos" ]; then
        log_success "Apple Silicon detected (will use Metal acceleration)"
    else
        log_warning "No NVIDIA GPU detected. CPU inference will be slower."
    fi
}

# Install Ollama
install_ollama() {
    log_info "Installing Ollama..."
    
    if command -v ollama &> /dev/null; then
        log_success "Ollama already installed: $(ollama --version)"
        return 0
    fi
    
    case "$OS" in
        macos|linux)
            curl -fsSL https://ollama.com/install.sh | sh
            ;;
        windows)
            log_error "Please download Ollama from https://ollama.com/download"
            exit 1
            ;;
        *)
            log_error "Unsupported OS: $OS"
            exit 1
            ;;
    esac
    
    log_success "Ollama installed successfully!"
}

# Start Ollama service
start_ollama() {
    log_info "Starting Ollama service..."
    
    if pgrep -x "ollama" > /dev/null; then
        log_success "Ollama is already running"
    else
        if [ "$OS" = "macos" ]; then
            ollama serve &>/dev/null &
            sleep 3
        else
            # Linux with systemd
            if command -v systemctl &> /dev/null; then
                sudo systemctl start ollama || ollama serve &>/dev/null &
            else
                ollama serve &>/dev/null &
            fi
            sleep 3
        fi
        log_success "Ollama service started"
    fi
}

# Pull models based on available RAM/VRAM
pull_models() {
    log_info "Pulling coding models..."
    
    # Always pull the small autocomplete model
    log_info "Pulling autocomplete model (Qwen 1.5B)..."
    ollama pull qwen2.5-coder:1.5b-base
    
    # Determine main model based on RAM
    if [ "$TOTAL_RAM" -ge 32 ]; then
        log_info "Pulling main model (Qwen 32B Q8 - best quality)..."
        ollama pull qwen2.5-coder:32b-instruct-q8_0
        MAIN_MODEL="qwen2.5-coder:32b-instruct-q8_0"
    elif [ "$TOTAL_RAM" -ge 24 ]; then
        log_info "Pulling main model (Qwen 32B Q4)..."
        ollama pull qwen2.5-coder:32b
        MAIN_MODEL="qwen2.5-coder:32b"
    elif [ "$TOTAL_RAM" -ge 16 ]; then
        log_info "Pulling main model (Qwen 14B)..."
        ollama pull qwen2.5-coder:14b
        MAIN_MODEL="qwen2.5-coder:14b"
    else
        log_info "Pulling main model (Qwen 7B - for limited RAM)..."
        ollama pull qwen2.5-coder:7b
        MAIN_MODEL="qwen2.5-coder:7b"
    fi
    
    # Pull embedding model for RAG
    log_info "Pulling embedding model..."
    ollama pull nomic-embed-text
    
    log_success "Models downloaded successfully!"
}

# Test Ollama
test_ollama() {
    log_info "Testing Ollama..."
    
    RESPONSE=$(curl -s http://localhost:11434/api/tags)
    if echo "$RESPONSE" | grep -q "models"; then
        log_success "Ollama is working! ✓"
    else
        log_error "Ollama test failed. Please check the logs."
        exit 1
    fi
}

# Create Continue.dev config
setup_continue() {
    log_info "Setting up Continue.dev configuration..."
    
    CONTINUE_DIR="$HOME/.continue"
    mkdir -p "$CONTINUE_DIR"
    
    cat > "$CONTINUE_DIR/config.json" << EOF
{
  "models": [
    {
      "title": "Qwen 32B (Local)",
      "provider": "ollama",
      "model": "$MAIN_MODEL",
      "contextLength": 32768
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen 1.5B (Fast)",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b-base"
  },
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text"
  },
  "allowAnonymousTelemetry": false
}
EOF
    
    log_success "Continue.dev config created at $CONTINUE_DIR/config.json"
}

# Print next steps
print_next_steps() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}   🎉 Setup Complete! Here's what to do next:              ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. Install Continue.dev extension in VS Code:"
    echo "   → Search for 'Continue' in Extensions marketplace"
    echo ""
    echo "2. Test your setup:"
    echo "   → ollama run $MAIN_MODEL"
    echo "   → Type: 'Write a Python function to find prime numbers'"
    echo ""
    echo "3. Start coding with AI:"
    echo "   → Open VS Code, press Cmd+L (Mac) or Ctrl+L (Windows/Linux)"
    echo "   → Ask Continue to help with your code!"
    echo ""
    echo "📚 Full guide: https://github.com/murataslan1/local-ai-coding-guide"
    echo ""
}

# Main execution
main() {
    print_banner
    detect_os
    check_requirements
    install_ollama
    start_ollama
    pull_models
    test_ollama
    setup_continue
    print_next_steps
}

# Run main function
main "$@"

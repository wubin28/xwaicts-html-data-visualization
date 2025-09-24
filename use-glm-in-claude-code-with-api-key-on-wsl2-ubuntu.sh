#!/usr/bin/env zsh

# WSL2 Ubuntu script to configure Claude Code to use GLM-4 model
# Usage: ./use-glm-in-claude-code-with-api-key-on-wsl2-ubuntu.sh

echo "Setting up environment variables for GLM-4 model on WSL2 Ubuntu..."

# Prompt for API key with secure input (hidden)
echo "Please enter your GLM API key:"
read -s API_KEY
echo "✓ API key entered ($(printf '%*s' ${#API_KEY} | tr ' ' '*'))"

echo "Configuring Claude Code to use GLM-4 model..."

# Set environment variables for GLM-4
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
export ANTHROPIC_AUTH_TOKEN=$API_KEY
export ANTHROPIC_MODEL=glm-4
export ANTHROPIC_SMALL_FAST_MODEL=glm-3-turbo

echo "✓ Set ANTHROPIC_BASE_URL"
echo "✓ Set ANTHROPIC_AUTH_TOKEN (secured)"
echo "✓ Set ANTHROPIC_MODEL to glm-4"
echo "✓ Set ANTHROPIC_SMALL_FAST_MODEL to glm-3-turbo"

echo ""
echo "Environment setup complete! You can now use GLM-4 model with Claude."
echo "Current environment variables:"
echo "ANTHROPIC_BASE_URL: $ANTHROPIC_BASE_URL"
echo "ANTHROPIC_MODEL: $ANTHROPIC_MODEL"
echo "ANTHROPIC_SMALL_FAST_MODEL: $ANTHROPIC_SMALL_FAST_MODEL"

# Launch Claude Code with the configured environment
echo "Launching Claude Code with GLM-4 configuration..."

# For WSL2, we need to check if we have Claude command available
if command -v claude >/dev/null 2>&1; then
    claude
elif command -v code >/dev/null 2>&1; then
    echo "Claude command not found, trying to launch VS Code with Claude extension..."
    code
else
    echo "⚠️  Neither 'claude' nor 'code' command found."
    echo "Please make sure Claude Code is installed and available in your PATH."
    echo "You can manually launch Claude Code now with the configured environment variables."
fi

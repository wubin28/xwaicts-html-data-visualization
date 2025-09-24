# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository is focused on AI agent performance analysis and data visualization. It contains:
- Excel dataset processing for AI agent performance metrics
- HTML dashboard generation for data visualization
- Configuration scripts for different AI models (Kimi K2, GLM-4)
- RIPER-5 workflow protocol for development

## Key Files and Structure

### Core Data Files
- `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` - Main dataset with 80 records containing AI agent performance metrics
- `data_processing.log` - Processing logs showing dataset analysis results

### Configuration Scripts
- `use-kimi-in-claude-code-with-api-key-on-wsl2-ubuntu.sh` - Configure Claude Code for Kimi K2 model on WSL2 Ubuntu
- `use-kimi-in-claude-code-with-api-key-on-mac.sh` - Configure Claude Code for Kimi K2 model on macOS
- `use-glm-in-claude-code-with-api-key-on-wsl2-ubuntu.sh` - Configure Claude Code for GLM-4 model on WSL2 Ubuntu
- PowerShell variants for Windows environments

### Development Protocol
- `rules-riper5.md` - Strict operational protocol with 5 modes (RESEARCH, INNOVATE, PLAN, EXECUTE, REVIEW)
- `requirements.md` - Project requirements for data dashboard generation
- `prompts.md` - Current task instructions following RIPER-5 workflow

## Common Development Commands

### Model Configuration
```bash
# Configure for Kimi K2 on WSL2 Ubuntu
./use-kimi-in-claude-code-with-api-key-on-wsl2-ubuntu.sh

# Configure for GLM-4 on WSL2 Ubuntu
./use-glm-in-claude-code-with-api-key-on-wsl2-ubuntu.sh

# Configure for Kimi K2 on macOS
./use-kimi-in-claude-code-with-api-key-on-mac.sh
```

### Data Processing
The repository processes Excel data to generate HTML dashboards. Key processing steps:
1. Read Excel file (`first-80-rows-agentic_ai_performance_dataset_20250622.xlsx`)
2. Analyze 3 specific metrics about AI agent performance
3. Generate `data-dashboard.html` with visualizations
4. Create `read-excel-data.py` for data processing code

## RIPER-5 Workflow Protocol

When working in this repository, you MUST follow the RIPER-5 protocol defined in `rules-riper5.md`:

1. **RESEARCH**: Information gathering only - read files, understand structure
2. **INNOVATE**: Brainstorm approaches - discuss ideas, seek feedback
3. **PLAN**: Create detailed technical specifications with exact changes
4. **EXECUTE**: Implement exactly what was planned (requires explicit permission)
5. **REVIEW**: Validate implementation against plan

**Critical Requirements:**
- Begin every response with mode declaration: `[MODE: MODE_NAME]`
- Only transition modes with explicit user signals
- In EXECUTE mode, follow plan with 100% fidelity
- In REVIEW mode, flag any deviation from plan

## Data Analysis Focus

The project analyzes AI agent performance across three dimensions:
1. Multimodal capability by agent type (top 3 rankings)
2. Multimodal capability by model architecture (top 3 rankings)
3. Bias detection medians by task category (top 3 rankings)

Expected output files:
- `data-dashboard.html` - Mobile-responsive HTML dashboard with charts
- `read-excel-data.py` - Python code for Excel data processing
- `dashboard_data.json` - Processed data for dashboard generation
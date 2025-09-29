# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based data visualization project for analyzing an AI agent performance dataset. The project generates HTML dashboards to visualize insights from Excel data files containing agent performance metrics.

## Development Environment

### Python Virtual Environment
- **Required**: Use the existing `venv` directory (already set up)
- **Activation**: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
- **Python Version**: Python 3.12

### Installed Dependencies
Key packages available in the virtual environment:
- `pandas` (2.3.2) - Data manipulation and analysis
- `openpyxl` (3.1.5) - Excel file reading
- `matplotlib` (3.10.6) - Static plotting
- `seaborn` (0.13.2) - Statistical visualization
- `plotly` (6.3.0) - Interactive plotting
- `numpy` (2.3.3) - Numerical computing

## Project Structure

### Core Files
- `requirements.md` - Project requirements (in Chinese)
- `prompts.md` - Instructions following Riper-5 workflow
- `rules-riper5.md` - Strict operational protocol with 5 modes (RESEARCH, INNOVATE, PLAN, EXECUTE, REVIEW)

### Workflow Management Files
- `todo.md` - Task tracking and implementation checklists
- `bubbles.md` - Progress logging and change summaries
- `bubbling-logs.md` - Development documentation

### Expected Outputs
- `read-excel-data.py` - Python script for data processing
- `data-dashboard.html` - HTML visualization dashboard

## Development Workflow

### Riper-5 Protocol
This project follows a strict 5-mode development protocol:

1. **RESEARCH** - Information gathering only
2. **INNOVATE** - Brainstorming approaches
3. **PLAN** - Detailed technical specifications
4. **EXECUTE** - Implementation following exact plan
5. **REVIEW** - Validation against plan

**Important**: Always declare your current mode at the start of responses using `[MODE: MODE_NAME]` format.

### Key Requirements
- **Virtual Environment**: Must use the existing `venv` directory
- **Data Source**: Excel file `@first-80-rows-agentic_ai_performance_dataset_20250622.xlsx`
- **Output Format**: Static HTML with embedded visualizations (no external dependencies)
- **Design**: Light color scheme, mobile-responsive
- **Language**: Requirements are in Chinese, but code should have English comments

### Security Notes
- Handle sudo password requests by pausing for user input
- Never expose or commit sensitive information
- Validate all file operations before execution

## Data Analysis Focus

The project analyzes three specific questions about AI agent performance:
1. Top 3 agent types by multimodal capability percentage
2. Top 3 model architectures by multimodal capability percentage
3. Top 3 task categories by bias detection median scores

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install additional packages (if needed)
pip install package_name

# Run Python scripts
python read-excel-data.py

# Deactivate virtual environment
deactivate
```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based data visualization project for analyzing an AI agent performance dataset. The project generates HTML dashboards to visualize insights from Excel data files containing agent performance metrics.

**Important**: This project is part of an AI coding tools performance evaluation, comparing various AI-assisted programming tools (Claude Code, CodeBuddy Code, etc.) through practical implementation tasks using the ICMwRIPER-5 methodology.

## Development Environment

### Python Virtual Environment
- **Required**: Use the existing `venv` directory (already set up)
- **Activation**: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
- **Python Version**: Python 3.12
- **Note**: Python command must be run within the activated venv. Direct `python` command may not work outside venv.

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
- `icm-story-template.md` - Project requirements template (in Chinese, specifies 3 research questions)
- `icmwriper-5.md` - Strict operational protocol with 5 modes (RESEARCH, INNOVATE, PLAN, EXECUTE, REVIEW)
- `icm-bubble-template.md` - Starting prompt template for each iteration
- `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` - Excel dataset (80 records)

### Workflow Management Files
- `todo-yyyy-mm-dd--hh-mm.md` - Timestamped task tracking files created during PLAN mode
- `icm-story-yyyy-mm-dd--hh-mm.md` - Timestamped story description for each iteration
- `icm-bubble-yyyy-mm-dd--hh-mm.md` - Timestamped starting prompts for each iteration

### Expected Outputs
- `analyze_data.py` - Python script for data processing
- `data-dashboard.html` - HTML visualization dashboard

## Development Workflow

### ICMwRIPER-5 (Iterative Context Management with RIPER-5) Method
This project follows a strict 6-phase development protocol:

1. **Iterative Context Management** - Iteratively review and update story description file `icm-story-yyyy-mm-dd--hh-mm.md` and starting prompt file `icm-bubble-yyyy-mm-dd--hh-mm.md` based on the current iteration story to align AI context, then send the prompts from `icm-bubble-yyyy-mm-dd--hh-mm.md` to AI
2. **RESEARCH** - Information gathering and file reading only (permitted: reading files, generating code to read files; forbidden: suggestions, implementations, planning)
3. **INNOVATE** - Brainstorming approaches without implementation (permitted: discussing ideas; forbidden: concrete planning, implementation details)
4. **PLAN** - Create comprehensive technical specifications and save to timestamped todo file (format: `todo-yyyy-mm-dd--hh-mm.md`) with numbered checklist
5. **EXECUTE** - Follow the plan exactly with no creative decisions. Work on todos one by one, marking them off. Keep each task simple and minimal. Append review section at end.
6. **REVIEW** - Validate implementation against the original plan. Flag any deviations using `⚠️DEVIATION DETECTED:` format. Conclude with `✅IMPLEMENTATION MATCHES PLAN EXACTLY` or `❌IMPLEMENTATION DEVIATES FROM PLAN`. Then go back to phase 1.

**Critical**: Always declare your current mode at the start of responses using `[MODE: MODE_NAME]` format.

### Getting Started with ICMwRIPER-5 Method
When starting a new iteration:
1. Copy `icm-bubble-template.md` and `icm-story-template.md`
2. Rename to `icm-bubble-yyyy-mm-dd--hh-mm.md` and `icm-story-yyyy-mm-dd--hh-mm.md` (using current timestamp)
3. Modify content according to the specific story of the current iteration
4. Send prompts from `icm-bubble-yyyy-mm-dd--hh-mm.md` to AI to start the iteration

### Key Requirements
- **Virtual Environment**: Must use the existing `venv` directory (never create a new one)
- **Data Source**: Excel file `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` (80 records)
- **Output Format**: Static HTML with embedded visualizations (no external dependencies)
- **Design**: Light color scheme, mobile-responsive, works on mobile browsers
- **Language**: Requirements are in Chinese, but code should have English comments
- **File Naming**:
  - Generated Python script must be named exactly `analyze_data.py`
  - Generated HTML file must be named exactly `data-dashboard.html`
  - Todo files must use format `todo-yyyy-mm-dd--hh-mm.md`

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
# Create and activate virtual environment (if needed)
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# Check Python version (must be in venv)
python --version

# List installed packages (must be in venv)
pip list

# Install additional packages (if needed)
pip install package_name

# Run the data processing script
python analyze_data.py    # Windows
python3 analyze_data.py   # macOS/Linux

# Open generated dashboard in browser
open data-dashboard.html      # macOS
start data-dashboard.html     # Windows
xdg-open data-dashboard.html  # Linux/WSL

# Deactivate virtual environment
deactivate
```

## ICMwRIPER-5 Protocol Details

**Purpose**: This protocol prevents unauthorized AI modifications by enforcing strict mode-based workflow.

### Mode Transition Requirements
Only transition modes with explicit signals:
- "ENTER RESEARCH MODE"
- "ENTER INNOVATE MODE"
- "ENTER PLAN MODE"
- "ENTER EXECUTE MODE"
- "ENTER REVIEW MODE"

### Critical Protocol Guidelines
- **Cannot** transition between modes without explicit permission
- **Must** declare current mode at the start of EVERY response with `[MODE: MODE_NAME]`
- In EXECUTE mode: follow the plan with 100% fidelity, immediately return to PLAN if deviation needed
- In REVIEW mode: flag even the smallest deviation with `⚠️DEVIATION DETECTED:` format, then return to phase 1 (Iterative Context Management)
- **No** authority to make independent decisions outside the declared mode

### PLAN Mode Checklist Format
```
IMPLEMENTATION CHECKLIST:
1. [Specific action 1]
2. [Specific action 2]
...
n. [Final action]
```

Save to `todo-yyyy-mm-dd--hh-mm.md` in project root.

Full protocol details are in `icmwriper-5.md`.

## Evaluation Context

This is part of an AI coding tools performance evaluation comparing various AI-assisted programming tools (Claude Code, CodeBuddy Code, etc.) through practical implementation tasks.

Each git branch represents a single evaluation session with metadata in the branch name. Example: `2025-09-28--20-09-satisfied-by-codebuddycode-with-default-deepseekv3.1-in-codebuddycn-on-wsl`

Branch name format indicates:
- **Timestamp**: Evaluation start time (2025-09-28--20-09)
- **Result**: Satisfaction level (satisfied/unsatisfied)
- **AI CLI Tool**: Tool used (codebuddycode, claudecode, etc.)
- **Model**: LLM configuration (default-deepseekv3.1, etc.)
- **AI IDE**: Development environment (codebuddycn, cursor, etc.)
- **Platform**: Operating system (wsl, mac, windows, etc.)
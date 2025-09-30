# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based data visualization project for analyzing an AI agent performance dataset. The project generates HTML dashboards to visualize insights from Excel data files containing agent performance metrics.

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
- `icm-story-template.md` - Project requirements template (in Chinese)
- `icm-riper-5.md` - Strict operational protocol with 5 modes (RESEARCH, INNOVATE, PLAN, EXECUTE, REVIEW)
- `icm-template.md` - Iterative Context Management template prompts
- `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` - Excel dataset (80 records)

### Workflow Management Files
- `todo.md` - Task tracking and implementation checklists
- `bubbles.md` - Progress logging and change summaries
- `bubbling-logs.md` - Development documentation

### Expected Outputs
- `read-excel-data.py` - Python script for data processing (NOT YET GENERATED)
- `data-dashboard.html` - HTML visualization dashboard (NOT YET GENERATED)

## Development Workflow

### ICM-RIPER-5 Protocol
This project follows a strict 6-phase development protocol with Iterative Context Management:

1. **Iterative Context Management** - Regularly review and update context files based on current iteration story
2. **RESEARCH** - Information gathering and file reading only
3. **INNOVATE** - Brainstorming approaches without implementation
4. **PLAN** - Create comprehensive technical specifications and save to timestamped todo file (format: `todo-yyyy-mm-dd--hh-mm.md`)
5. **EXECUTE** - Follow the plan exactly with no creative decisions
6. **REVIEW** - Validate implementation against the original plan

**Critical**: Always declare your current mode at the start of responses using `[MODE: MODE_NAME]` format.

### Iterative Context Management
The `icm-template.md` file serves as an Iterative Context Management template. When starting a new iteration:
1. Copy the `icm-template.md` file
2. Rename it to `icm-yyyy-mm-dd--hh-mm.md` (using current timestamp)
3. Modify the content according to the specific story of the current iteration

### Key Requirements
- **Virtual Environment**: Must use the existing `venv` directory (never create a new one)
- **Data Source**: Excel file `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` (80 records)
- **Output Format**: Static HTML with embedded visualizations (no external dependencies)
- **Design**: Light color scheme, mobile-responsive, works on mobile browsers
- **Language**: Requirements are in Chinese, but code should have English comments
- **File Naming**:
  - Generated Python script must be named exactly `read-excel-data.py`
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
# Activate virtual environment
source venv/bin/activate

# Install additional packages (if needed)
pip install package_name

# Run the data processing script
python read-excel-data.py

# Open generated dashboard in browser
# Linux/WSL
xdg-open data-dashboard.html
# macOS
open data-dashboard.html
# Windows
start data-dashboard.html

# Check Python version (must be in venv)
python --version

# List installed packages (must be in venv)
pip list

# Deactivate virtual environment
deactivate
```

## ICM-RIPER-5 Protocol Details

The project strictly follows the ICM-RIPER-5 methodology defined in `icm-riper-5.md`:

1. **RESEARCH** - Information gathering and file reading only (including generating code such as python to read files)
2. **INNOVATE** - Brainstorming approaches without implementation
3. **PLAN** - Create comprehensive technical specifications and save to timestamped todo file (`todo-yyyy-mm-dd--hh-mm.md`)
4. **EXECUTE** - Follow the plan exactly with no creative decisions. Work on todos one by one, marking them off as completed. Keep each task simple and minimal. Append a review section at the end of the todo file summarizing changes.
5. **REVIEW** - Validate implementation against the original plan. Flag any deviations using `⚠️DEVIATION DETECTED:` format. Conclude with `✅IMPLEMENTATION MATCHES PLAN EXACTLY` or `❌IMPLEMENTATION DEVIATES FROM PLAN`.

**Critical Protocol Guidelines**:
- Cannot transition between modes without explicit permission
- Must declare current mode at the start of EVERY response
- In EXECUTE mode, must follow the plan with 100% fidelity
- In REVIEW mode, must flag even the smallest deviation
- No authority to make independent decisions outside the declared mode

**Mode Transition Signals**:
- "ENTER RESEARCH MODE"
- "ENTER INNOVATE MODE"
- "ENTER PLAN MODE"
- "ENTER EXECUTE MODE"
- "ENTER REVIEW MODE"

## Evaluation Context

This is part of an AI coding tools performance evaluation. Each git branch represents a single evaluation session with metadata in the branch name indicating:
- Timestamp of evaluation
- Result satisfaction level
- AI tool used
- LLM model configuration
- Platform details
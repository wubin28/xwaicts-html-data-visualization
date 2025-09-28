# CodeBuddy Code Configuration

## Project Overview
This is a data visualization project that creates an HTML dashboard from an Excel dataset ("Agentic AI Performance Dataset 2025"). The project focuses on analyzing AI agent performance data and generating a static HTML dashboard with visualizations.

## Key Files
- **Dataset**: `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` - The main dataset with 80 records
- **Requirements**: `requirements.md` - Project requirements and analysis questions
- **Workflow Rules**: `rules-riper5.md` - Strict operational protocol for development
- **Scripts**: Various API key setup scripts for different AI models (DeepSeek, GLM, Kimi)

## Development Workflow
This project follows the RIPER-5 strict operational protocol:

### Mode Transitions (Must be explicitly requested):
1. **RESEARCH** - Information gathering only
2. **INNOVATE** - Brainstorming potential approaches  
3. **PLAN** - Create exhaustive technical specification
4. **EXECUTE** - Implement exactly what was planned
5. **REVIEW** - Ruthlessly validate implementation against plan

**Important**: Always begin responses with `[MODE: MODE_NAME]` as specified in the protocol.

## Development Setup

### Virtual Environment
- Create virtual environment in `venv/` directory
- Always use this specific directory name for the virtual environment
- Install Python dependencies within this environment

### Python Development
- Target file: `read-excel-data.py` (for data analysis)
- Dependencies: pandas, openpyxl for Excel processing
- Data analysis focuses on:
  - Agent type rankings by multimodal capability
  - Model architecture rankings by multimodal capability  
  - Task category rankings by bias detection median

### HTML Dashboard
- Target file: `data-dashboard.html`
- Requirements: Static HTML, light color theme, mobile-responsive
- Must display actual processed record count
- No dynamic effects or external file dependencies

## Key Analysis Questions
1. Top 3 agent types by multimodal capability percentage
2. Top 3 model architectures by multimodal capability percentage  
3. Top 3 task categories by bias detection median

## Project Structure
- Data processing and analysis in Python
- Static HTML dashboard generation
- Workflow tracking through bubbles.md and todo.md files
- Strict adherence to RIPER-5 protocol for all development tasks
# Xiao Wu AI Coding Tools Showdown by Generating HTML Data Dashboard

A Python-based project for analyzing and visualizing AI agent performance metrics from Excel datasets, generating interactive HTML dashboards.

## Project Purpose

This project evaluates the performance of various AI-assisted programming tools and their associated large language models through practical implementation challenges. Rather than relying solely on programming competition scores, we assess these rapidly evolving AI coding tools through real-world tasks that generate HTML data visualization dashboards, providing meaningful insights into their actual capabilities and effectiveness.

## Evaluation Methodology

Each Git branch represents a single evaluation session, with branch names containing comprehensive evaluation metadata. For example, the branch `2025-09-28--20-09-satisfied-by-codebuddycode-with-default-deepseekv3.1-in-codebuddycn-on-wsl` indicates:

- **Timestamp**: Evaluation started on September 28, 2025, at 20:09
- **Result**: "satisfied" - indicating satisfactory performance
- **AI CLI Tool**: CodeBuddy Code IDE
- **Model**: Default configuration with DeepSeek v3.1 large language model
- **AI IDE**: CodeBuddyCN (China domestic version) built-in terminal
- **Platform**: Windows 11 WSL2 Ubuntu 24.04

This systematic naming convention enables tracking and comparison of different AI tool combinations across various environments and configurations.

## Project Description

This project processes and visualizes data from the "Agentic AI Performance Dataset 2025" to answer three key research questions about AI agent capabilities:

1. **Multimodal Agent Types**: Top 3 agent types by multimodal processing capability percentage
2. **Multimodal Architectures**: Top 3 model architectures by multimodal processing capability percentage
3. **Bias Detection Performance**: Top 3 task categories by bias detection median scores

## Features

- Excel data processing and analysis
- Interactive HTML dashboard generation
- Mobile-responsive design with light color scheme
- Static output (no external dependencies required)
- Comprehensive data visualization using multiple chart types

## Requirements

- Python 3.12
- Virtual environment (pre-configured)
- Excel dataset: `first-80-rows-agentic_ai_performance_dataset_20250622.xlsx` (80 records)

## Installation & Setup

1. **Activate the virtual environment:**
   ```bash
   # Linux/macOS
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

2. **Verify installed packages and Python version:**
   ```bash
   python --version
   pip list
   ```

## Dependencies

The project includes these pre-installed packages:

- **pandas** (2.3.2) - Data manipulation and analysis
- **openpyxl** (3.1.5) - Excel file reading
- **matplotlib** (3.10.6) - Static plotting
- **seaborn** (0.13.2) - Statistical visualization
- **plotly** (6.3.0) - Interactive plotting
- **numpy** (2.3.3) - Numerical computing

## Usage

1. **Run the data analysis script:**
   ```bash
   python read-excel-data.py
   ```

2. **Open the generated dashboard:**
   ```bash
   # Open data-dashboard.html in your browser
   open data-dashboard.html      # macOS
   start data-dashboard.html     # Windows
   xdg-open data-dashboard.html  # Linux/WSL
   ```

## Output Files

- `read-excel-data.py` - Python script for data processing and analysis
- `data-dashboard.html` - Interactive HTML dashboard with visualizations

## Development Workflow

This project follows the **ICM-RIPER-5 Protocol** with five distinct development phases:

1. **RESEARCH** - Information gathering and file reading only
2. **INNOVATE** - Brainstorming approaches without implementation
3. **PLAN** - Create comprehensive technical specifications and save to timestamped todo file
4. **EXECUTE** - Follow the plan exactly with no creative decisions
5. **REVIEW** - Validate implementation against the original plan

**Critical**: AI assistants must declare their current mode with `[MODE: MODE_NAME]` at the start of each response.

### Iterative Context Management (ICM)

The `icm-template.md` file serves as an Iterative Context Management template with prompt instructions. When first using this template:

1. Copy the `icm-template.md` file
2. Rename it to `icm-yyyy-mm-dd--hh-mm.md` (using current timestamp)
3. Modify the content according to the specific requirements of the current iteration

This approach ensures each development iteration has customized context and prompts while maintaining consistency with the overall project structure.

## Project Structure

```
├── venv/                                                    # Python virtual environment
├── icm-requirements.md                                      # Project requirements (Chinese)
├── icm-riper-5.md                                          # ICM-RIPER-5 development protocol
├── prompts-final-result.md                                 # Generating the code for the final result without using RIPER-5
├── icm-template.md                                         # Iterative Context Management template prompts
├── first-80-rows-agentic_ai_performance_dataset_20250622.xlsx # Excel dataset (80 records)
├── todo.md                                                 # Task tracking
├── bubbles.md                                              # Progress logging
├── bubbling-logs.md                                        # Development documentation
├── CLAUDE.md                                               # AI assistant guidance
├── README.md                                               # Project documentation
├── read-excel-data.py                                      # Data processing script (generated)
└── data-dashboard.html                                     # Visualization dashboard (generated)
```

## Data Analysis Focus

The dashboard provides insights into:

- **Agent Type Analysis**: Distribution and capabilities of different AI agent types
- **Architecture Performance**: Comparison of model architectures and their multimodal capabilities
- **Bias Detection Metrics**: Fairness performance across different task categories
- **Statistical Summaries**: Comprehensive data overview and key metrics

## Technical Notes

- All visualizations are embedded in the HTML file (no external dependencies)
- Mobile-responsive design ensures compatibility across devices
- Light color scheme optimized for readability
- Dataset contains 80 records of AI agent performance data

## Contributing

When working on this project:

1. Always use the existing `venv` virtual environment
2. Follow the ICM-RIPER-5 development protocol strictly
3. Always declare your current mode with `[MODE: MODE_NAME]`
4. Generated files must be named exactly `read-excel-data.py` and `data-dashboard.html`
5. Ensure all outputs are self-contained HTML files with no external dependencies
6. Maintain mobile responsiveness and light color themes
7. Code comments should be in English, even though requirements are in Chinese

## Security

- Handle sensitive operations with appropriate user confirmation
- Never commit API keys or sensitive data
- Validate all file operations before execution
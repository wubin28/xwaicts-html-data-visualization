# Agentic AI Performance Dataset 2025 Data Processor

This project provides a Python script to read and process the Agentic AI Performance Dataset 2025 Excel file, perform required data analysis, and output results in JSON format.

## Files Overview

### Main Scripts
- **`read-excel-data.py`** - Primary script using pandas for optimal performance
- **`read-excel-data-stdlib.py`** - Fallback script using only Python standard library

### Output Files
- **`dashboard_data.json`** - JSON output with processed data and analysis results
- **`data_processing.log`** - Log file with detailed processing information

### Supporting Files
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - This documentation file

## Prerequisites

### Option 1: Full Version (Recommended)
Install required packages:
```bash
pip install pandas openpyxl
```

### Option 2: Standard Library Version
No additional packages required - uses only Python standard library.

## Usage

### Running the Full Version
```bash
python3 read-excel-data.py
```

### Running the Standard Library Version
```bash
python3 read-excel-data-stdlib.py
```

## Data Analysis Performed

The script performs three main analyses:

### 1. Agent Type Multimodal Capability Ranking
- **Purpose**: Identify which agent types have the highest percentage of multimodal capability
- **Output**: Top 3 agent types ranked by multimodal capability percentage
- **Columns Used**: `agent_type`, `multimodal_capability`

### 2. Model Architecture Multimodal Capability Ranking
- **Purpose**: Identify which model architectures have the highest percentage of multimodal capability
- **Output**: Top 3 model architectures ranked by multimodal capability percentage
- **Columns Used**: `model_architecture`, `multimodal_capability`

### 3. Task Category Bias Detection Ranking
- **Purpose**: Identify which task categories have the highest median bias detection scores
- **Output**: Top 3 task categories ranked by median bias detection score
- **Columns Used**: `task_category`, `bias_detection`

## Output Format

The script generates a JSON file (`dashboard_data.json`) with the following structure:

```json
{
  "dataset_summary": {
    "total_rows": 80,
    "total_columns": 5,
    "columns": ["agent_type", "model_architecture", "task_category", "multimodal_capability", "bias_detection"],
    "missing_values": {...},
    "unique_values": {...},
    "processing_timestamp": "2025-09-24T19:30:02.287955",
    "source_file": "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
  },
  "agent_type_multimodal_ranking": [
    {
      "agent_type": "Autonomous Agent",
      "total_count": 20,
      "multimodal_count": 20,
      "percentage": 100.0
    }
  ],
  "model_architecture_multimodal_ranking": [...],
  "task_category_bias_ranking": [...],
  "metadata": {
    "processing_timestamp": "2025-09-24T19:30:02.288793",
    "python_version": "3.12.3",
    "total_processed_records": 80
  }
}
```

## Error Handling and Logging

The script includes comprehensive error handling:

- **File validation**: Checks if Excel file exists and is readable
- **Data validation**: Validates required columns and data types
- **Exception handling**: Gracefully handles various error scenarios
- **Logging**: Detailed logging to both console and log file

### Log File
All processing activities are logged to `data_processing.log` with timestamps and severity levels.

## Script Features

### Data Processing
- **File validation**: Validates Excel file before processing
- **Data cleaning**: Handles missing values, standardizes formats
- **Memory efficiency**: Processes data efficiently for large datasets

### Analysis Functions
- **Agent type analysis**: Calculates multimodal capability percentages by agent type
- **Model architecture analysis**: Calculates multimodal capability percentages by architecture
- **Task category analysis**: Calculates median bias detection scores by task category

### Output Options
- **JSON export**: Saves results in structured JSON format
- **Console output**: Displays key findings during execution
- **Detailed logging**: Comprehensive logging for debugging

## Expected Dataset Structure

The Excel file should contain the following columns:
- `agent_type`: Type of AI agent (e.g., "Autonomous Agent", "Collaborative Agent")
- `model_architecture`: Architecture of the model (e.g., "Transformer", "CNN", "RNN")
- `task_category`: Category of task being performed (e.g., "Text Analysis", "Image Recognition")
- `multimodal_capability`: Whether the agent supports multimodal processing ("Yes"/"No")
- `bias_detection`: Score representing bias detection capability (numeric value)

## Sample Output

```
✅ Data processing completed successfully!
📊 Processed 80 records
💾 Results saved to dashboard_data.json

📈 Key Findings:
Top 3 Agent Types with Multimodal Capability:
  1. Autonomous Agent: 100.0%
  2. Reactive Agent: 100.0%
  3. Collaborative Agent: 0.0%

Top 3 Model Architectures with Multimodal Capability:
  1. Transformer: 100.0%
  2. RNN: 100.0%
  3. CNN: 0.0%

Top 3 Task Categories by Median Bias Detection Score:
  1. Image Recognition: 70.0
  2. Multimodal: 70.0
  3. Text Analysis: 69.0
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install required packages using pip
2. **File not found**: Ensure Excel file is in the same directory as the script
3. **Permission errors**: Ensure write permissions for output files

### Debug Mode
For detailed debugging information, check the `data_processing.log` file.

## Author

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
# Data Dashboard Generation Task - English Translation

## Original Requirements (Translated from Chinese):

I have a Kaggle dataset named "@first-80-rows-agentic_ai_performance_dataset_20250622.xlsx" called "Agentic AI Performance Dataset 2025", focusing on 3 questions about AI agent performance:

(1) Among agent types that support multimodal processing (multimodal_capability), which are the top three agent types ranked by the proportion within their respective agent type?

(2) Among model architectures that support multimodal processing (multimodal_capability), which are the top three model architectures ranked by the proportion within their respective model architecture?

(3) For various agent task categories (task_category), which are the top three task categories ranked by the median of agent performance fairness (bias detection) from highest to lowest?

I want to visualize this dataset. Please help me read this Excel file and generate a comprehensive data dashboard in HTML format named "data-dashboard.html".

The dashboard should include data visualization designs and display the actual total number of records processed (this dataset has 80 records in total, please only show the actual number of data rows read and processed).

Please use a light color scheme for the dashboard, provide directly runnable HTML static code.

No need to provide dynamic effects or use static images, and do not rely on loading Excel files to run the HTML code. Ensure all charts can be fully displayed in mobile browsers.

Please save the Python code used to read the Excel dataset and analyze the data to a file named "read-excel-data.py" so I can run and check the code later.

## Development Environment Requirements:
- Must create a virtual environment named "venv" in the project root directory (other names are prohibited)
- Install all necessary dependency packages in the venv virtual environment
- All code execution must be performed in the activated venv environment

## Safety Operation Specifications:
- If sudo privileges are required (such as installing system-level dependencies), immediately pause and prompt for password input
- Password input will be displayed as asterisks (*) to protect privacy
- Do not skip or modify any security verification steps
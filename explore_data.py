import pandas as pd

# Load the Excel file with row 1 (0-indexed) as the header
file_path = 'first-80-rows-agentic_ai_performance_dataset_20250622.xlsx'
df = pd.read_excel(file_path, header=1)  # Using row 1 (second row) as header

# Display basic information about the dataset
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nBasic statistics for numeric columns:")
print(df.describe())
print("\nMissing values:")
print(df.isnull().sum())

# Check for the specific columns mentioned in the requirements
columns_of_interest = ['agent_type', 'model_architecture', 'multimodal_capability', 'task_category', 'bias_detection_score']
print(f"\nColumns of interest:")
for col in columns_of_interest:
    if col in df.columns:
        print(f"✓ '{col}' exists in the dataset")
        print(f"  Unique values: {df[col].nunique()}")
        print(f"  Sample values: {df[col].dropna().unique()[:10].tolist()}")
    else:
        print(f"✗ '{col}' NOT found in the dataset")
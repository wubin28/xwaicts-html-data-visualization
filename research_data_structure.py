import pandas as pd
import numpy as np

def analyze_excel_structure():
    """Research mode: Examine Excel file structure and data format"""
    
    # Read the Excel file
    try:
        df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')
        print("✓ Excel file loaded successfully")
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return
    
    # Basic structure analysis
    print("\n=== DATASET STRUCTURE ANALYSIS ===")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    # Column names and data types
    print("\n=== COLUMN INFORMATION ===")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col} ({df[col].dtype})")
    
    # Sample data (first 5 rows)
    print("\n=== SAMPLE DATA (First 5 rows) ===")
    print(df.head())
    
    # Key columns verification
    key_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 'task_category', 'bias_detection']
    print("\n=== KEY COLUMNS VERIFICATION ===")
    for col in key_columns:
        if col in df.columns:
            print(f"✓ {col} - Found")
            print(f"  Data type: {df[col].dtype}")
            print(f"  Unique values: {df[col].nunique()}")
            print(f"  Sample values: {df[col].unique()[:5]}")
        else:
            print(f"❌ {col} - Not found")
    
    # Missing values analysis
    print("\n=== DATA QUALITY ANALYSIS ===")
    missing_data = df.isnull().sum()
    print("Missing values per column:")
    for col, missing in missing_data.items():
        if missing > 0:
            print(f"  {col}: {missing} missing values")
    
    if missing_data.sum() == 0:
        print("✓ No missing values found")
    
    # Data format observations
    print("\n=== DATA FORMAT OBSERVATIONS ===")
    if 'multimodal_capability' in df.columns:
        print(f"multimodal_capability format: {df['multimodal_capability'].unique()}")
    
    if 'bias_detection' in df.columns:
        print(f"bias_detection format: {df['bias_detection'].dtype}")
        print(f"bias_detection range: {df['bias_detection'].min()} to {df['bias_detection'].max()}")
    
    return df

if __name__ == "__main__":
    df = analyze_excel_structure()
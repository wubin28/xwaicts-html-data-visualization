import pandas as pd

def analyze_excel_structure_corrected():
    """Research mode: Examine Excel file with proper header handling"""
    
    # Read Excel file with first row as headers
    try:
        df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=0)
        print("✓ Excel file loaded with header=0")
        
        # If still showing unnamed columns, try header=1
        if 'Unnamed' in str(df.columns):
            df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=1)
            print("✓ Excel file reloaded with header=1")
            
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return
    
    print(f"\n=== CORRECTED DATASET STRUCTURE ===")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    print(f"\n=== ACTUAL COLUMN NAMES ===")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    # Check for our target columns
    target_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 'task_category', 'bias_detection']
    print(f"\n=== TARGET COLUMNS SEARCH ===")
    for target in target_columns:
        found_cols = [col for col in df.columns if target.lower() in str(col).lower()]
        if found_cols:
            print(f"✓ Found similar to '{target}': {found_cols}")
        else:
            print(f"❌ No match for '{target}'")
    
    return df

if __name__ == "__main__":
    df = analyze_excel_structure_corrected()
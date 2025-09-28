#!/usr/bin/env python3
"""
Script to analyze the actual structure of the Excel file by examining the data content.
"""

import pandas as pd
import os

def analyze_excel_structure():
    """Analyze the Excel file structure by examining the actual data content."""
    
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return
    
    print("=== Excel File Structure Analysis ===")
    print(f"File: {excel_file}")
    print()
    
    try:
        # Read the first few rows to see the actual structure
        df_raw = pd.read_excel(excel_file, header=None, nrows=5)
        
        print("First 5 rows of raw data (without header interpretation):")
        print(df_raw)
        print()
        
        # The first row appears to be the actual column headers
        # Let's examine what each column contains
        print("Examining what each column contains:")
        print()
        
        # Read the file with the first row as headers
        df = pd.read_excel(excel_file, header=0)
        
        # The first row after header contains the actual column descriptions
        # Let's see what's in each column
        for i, col_name in enumerate(df.columns):
            print(f"Column {i}: {col_name}")
            
            # Look at the first few non-null values in this column
            values = df[col_name].dropna().head(3)
            if len(values) > 0:
                print(f"  First values: {list(values)}")
            
            # Check if this column might contain our required data
            col_lower = str(col_name).lower()
            if 'agent' in col_lower and 'type' in col_lower:
                print("  → This might be 'agent_type'")
            elif 'multimodal' in col_lower:
                print("  → This might be 'multimodal_capability'")
            elif 'model' in col_lower and 'architect' in col_lower:
                print("  → This might be 'model_architecture'")
            elif 'task' in col_lower and 'categor' in col_lower:
                print("  → This might be 'task_category'")
            elif 'bias' in col_lower:
                print("  → This might be 'bias detection'")
            
            print()
        
        # Let's also look at the actual data starting from row 2 (index 1)
        print("Actual data starting from row 2:")
        print(df.iloc[1:4])  # Show rows 2-4
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_excel_structure()
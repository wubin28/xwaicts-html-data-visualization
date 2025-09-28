#!/usr/bin/env python3
"""
Script to correctly read the Excel file structure and identify the actual column names.
"""

import pandas as pd
import os

def read_excel_correctly():
    """Read the Excel file correctly by identifying the actual column names."""
    
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return
    
    print("=== Correct Excel File Reading ===")
    print(f"File: {excel_file}")
    print()
    
    try:
        # Read the first two rows to see the column names
        df_first_rows = pd.read_excel(excel_file, header=None, nrows=2)
        
        print("First two rows (column names and first data row):")
        print(df_first_rows)
        print()
        
        # The first row (index 0) contains the actual column names
        column_names = df_first_rows.iloc[0].tolist()
        
        print("Actual column names from first row:")
        for i, col_name in enumerate(column_names):
            print(f"Column {i}: {col_name}")
        print()
        
        # Now read the data starting from row 2 (index 1) with proper column names
        df = pd.read_excel(excel_file, header=0)
        
        # Remove the first row (which has the column descriptions) and set proper column names
        df_clean = df.iloc[1:].copy()
        df_clean.columns = column_names
        
        print(f"Actual data rows: {len(df_clean)}")
        print(f"Columns: {len(df_clean.columns)}")
        print()
        
        print("First 5 rows of cleaned data:")
        print(df_clean.head())
        print()
        
        print("Column names in cleaned data:")
        for i, col in enumerate(df_clean.columns):
            print(f"{i}: {col}")
        print()
        
        # Check for the specific columns mentioned in requirements
        print("Searching for columns with relevant keywords:")
        required_terms = ['agent_type', 'multimodal', 'model_architecture', 'task_category', 'bias']
        
        for col in df_clean.columns:
            col_lower = str(col).lower()
            for term in required_terms:
                if term in col_lower:
                    print(f"✓ Found '{term}' in column: {col}")
                    
        # Check data types
        print("\nData types:")
        print(df_clean.dtypes)
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    read_excel_correctly()
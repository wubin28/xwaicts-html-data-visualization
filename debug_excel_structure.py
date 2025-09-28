#!/usr/bin/env python3
"""
Debug script to understand the actual Excel file structure.
"""

import pandas as pd
import os

def debug_excel_structure():
    """Debug the Excel file structure to understand the actual column names."""
    
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return
    
    print("=== Debug Excel File Structure ===")
    print(f"File: {excel_file}")
    print()
    
    try:
        # Read the first 5 rows as raw data to understand the structure
        df_raw = pd.read_excel(excel_file, header=None, nrows=5)
        
        print("First 5 rows as raw data:")
        print(df_raw)
        print()
        
        # Look at each row individually
        print("Row 0 (index 0):")
        print(df_raw.iloc[0])
        print()
        
        print("Row 1 (index 1):")
        print(df_raw.iloc[1])
        print()
        
        print("Row 2 (index 2):")
        print(df_raw.iloc[2])
        print()
        
        # Check if row 1 contains the actual column names
        print("Row 1 values (potential column names):")
        for i, value in enumerate(df_raw.iloc[1]):
            print(f"Column {i}: {value}")
        
        # Try reading with different header parameters
        print("\nTrying header=1 (using second row as column names):")
        df_header1 = pd.read_excel(excel_file, header=1)
        print(f"Shape: {df_header1.shape}")
        print("Column names:")
        for i, col in enumerate(df_header1.columns):
            print(f"{i}: {col}")
        print()
        
        print("First 3 rows of data:")
        print(df_header1.head(3))
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_excel_structure()
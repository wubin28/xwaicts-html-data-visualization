#!/usr/bin/env python3
"""
Script to examine the Excel file structure more carefully.
"""

import pandas as pd
import os

def examine_excel_file_detailed():
    """Examine the Excel file structure with different reading parameters."""
    
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return
    
    print("=== Detailed Excel File Examination ===")
    print(f"File: {excel_file}")
    print()
    
    try:
        # First, let's see what's in the first few rows as raw data
        print("Reading first 10 rows without header to see actual data structure:")
        df_raw = pd.read_excel(excel_file, header=None, nrows=10)
        print(df_raw)
        print()
        
        # Now let's read with header=0 to see if the first row contains column names
        print("Reading with header=0 (using first row as column names):")
        df_with_header = pd.read_excel(excel_file, header=0)
        print(f"Number of rows: {len(df_with_header)}")
        print(f"Number of columns: {len(df_with_header.columns)}")
        print()
        
        print("Column names after reading with header=0:")
        for i, col in enumerate(df_with_header.columns):
            print(f"{i}: {col}")
        print()
        
        # Check if we have the columns we need
        column_names = df_with_header.columns.tolist()
        print("All column names:")
        print(column_names)
        print()
        
        # Look for columns that might contain our required data
        required_keywords = ['agent', 'multimodal', 'model', 'task', 'bias']
        
        print("Searching for columns with relevant keywords:")
        for col in column_names:
            if any(keyword in str(col).lower() for keyword in required_keywords):
                print(f"✓ Found relevant column: {col}")
        print()
        
        # Let's see the actual data structure
        print("First 3 rows of actual data:")
        print(df_with_header.head(3))
        print()
        
        # Check data types and basic info
        print("Data types:")
        print(df_with_header.dtypes)
        print()
        
        # Basic statistics
        print("Basic info about the dataset:")
        print(df_with_header.info())
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    examine_excel_file_detailed()
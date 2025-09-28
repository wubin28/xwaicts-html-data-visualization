#!/usr/bin/env python3
"""
Script to examine the Excel file structure and understand the data columns.
This script will help us understand the dataset before creating the main analysis script.
"""

import pandas as pd
import os

def examine_excel_file():
    """Examine the Excel file structure and content."""
    
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return
    
    print("=== Excel File Examination ===")
    print(f"File: {excel_file}")
    print()
    
    # Read the Excel file
    try:
        # First, let's see what sheets are available
        xl = pd.ExcelFile(excel_file)
        print(f"Available sheets: {xl.sheet_names}")
        print()
        
        # Read the first sheet (assuming it's the main data)
        df = pd.read_excel(excel_file)
        
        # Basic information about the dataset
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print()
        
        # Column names and data types
        print("Column names and data types:")
        print(df.dtypes)
        print()
        
        # First few rows to understand the data structure
        print("First 5 rows of data:")
        print(df.head())
        print()
        
        # Check for the specific columns mentioned in requirements
        required_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 'task_category', 'bias detection']
        
        print("Checking for required columns:")
        for col in required_columns:
            if col in df.columns:
                print(f"✓ Found: {col}")
            else:
                print(f"✗ Missing: {col}")
        
        print()
        
        # Basic statistics for numerical columns
        print("Basic statistics for numerical columns:")
        print(df.describe())
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    examine_excel_file()
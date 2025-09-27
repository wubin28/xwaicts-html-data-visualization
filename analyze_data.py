# Agentic AI Performance Data Dashboard Generator
# Educational Python script for beginners learning data analysis and web development
# This script reads Excel data, performs analysis, and generates an HTML dashboard

# Import required libraries
import pandas as pd  # For data manipulation and analysis
import json         # For converting Python data to JavaScript format

# Step 1: Import libraries completed
print("✓ Libraries imported successfully")

def load_and_validate_data():
    """
    Function to load Excel data and validate it for beginners
    This function demonstrates how to read Excel files and check data quality
    """
    print("\n=== STEP 2: Loading and Validating Data ===")
    
    try:
        # Load the Excel file - header=1 means the second row contains column names
        # This is a common issue with Excel files that have title rows
        df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=1)
        print("✓ Excel file loaded successfully")
        
        # Check the basic structure of our data
        total_rows = len(df)
        total_columns = len(df.columns)
        print(f"✓ Dataset contains {total_rows} rows and {total_columns} columns")
        
        # Validate we have the expected 80 rows
        if total_rows == 80:
            print("✓ Confirmed: Dataset has exactly 80 rows as expected")
        else:
            print(f"⚠ Warning: Expected 80 rows, but found {total_rows} rows")
        
        # Check if all required columns exist for our analysis
        required_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 
                          'task_category', 'bias_detection_score']
        
        missing_columns = []
        for column in required_columns:
            if column in df.columns:
                print(f"✓ Found required column: {column}")
            else:
                missing_columns.append(column)
                print(f"❌ Missing required column: {column}")
        
        if missing_columns:
            print(f"❌ Error: Missing columns {missing_columns}")
            return None
        
        print("✓ All required columns found - data is ready for analysis")
        return df
        
    except FileNotFoundError:
        print("❌ Error: Excel file not found. Please check the file name and location.")
        return None
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return None

def analyze_agent_types_multimodal(df):
    """
    Analyze which agent types have the highest multimodal capability support
    This function teaches groupby operations and percentage calculations
    """
    print("\n=== STEP 3: Analyzing Agent Types Multimodal Support ===")
    
    # Group the data by agent_type to analyze each type separately
    # This is like sorting data into different piles based on agent type
    agent_groups = df.groupby('agent_type')
    print(f"✓ Found {len(agent_groups)} different agent types")
    
    # Calculate multimodal support percentage for each agent type
    multimodal_percentages = {}
    
    for agent_type, group_data in agent_groups:
        # Count total agents of this type
        total_agents = len(group_data)
        
        # Count how many support multimodal (True values)
        multimodal_count = group_data['multimodal_capability'].sum()
        
        # Calculate percentage (multiply by 100 to get percentage)
        percentage = (multimodal_count / total_agents) * 100
        
        multimodal_percentages[agent_type] = round(percentage, 1)
        print(f"  {agent_type}: {multimodal_count}/{total_agents} = {percentage:.1f}%")
    
    # Sort by percentage (highest first) and get top 3
    # sorted() function sorts items, reverse=True means highest first
    sorted_results = sorted(multimodal_percentages.items(), key=lambda x: x[1], reverse=True)
    top_3_agent_types = sorted_results[:3]  # [:3] means first 3 items
    
    print("\n✓ Top 3 Agent Types by Multimodal Support:")
    for i, (agent_type, percentage) in enumerate(top_3_agent_types, 1):
        print(f"  {i}. {agent_type}: {percentage}%")
    
    return top_3_agent_types

def analyze_model_architectures_multimodal(df):
    """
    Analyze which model architectures have the highest multimodal capability support
    Similar to agent types analysis but for model architectures
    """
    print("\n=== STEP 4: Analyzing Model Architectures Multimodal Support ===")
    
    # Group by model_architecture - same concept as agent types
    architecture_groups = df.groupby('model_architecture')
    print(f"✓ Found {len(architecture_groups)} different model architectures")
    
    # Calculate multimodal support percentage for each architecture
    multimodal_percentages = {}
    
    for architecture, group_data in architecture_groups:
        total_models = len(group_data)
        multimodal_count = group_data['multimodal_capability'].sum()
        percentage = (multimodal_count / total_models) * 100
        
        multimodal_percentages[architecture] = round(percentage, 1)
        print(f"  {architecture}: {multimodal_count}/{total_models} = {percentage:.1f}%")
    
    # Sort and get top 3 architectures
    sorted_results = sorted(multimodal_percentages.items(), key=lambda x: x[1], reverse=True)
    top_3_architectures = sorted_results[:3]
    
    print("\n✓ Top 3 Model Architectures by Multimodal Support:")
    for i, (architecture, percentage) in enumerate(top_3_architectures, 1):
        print(f"  {i}. {architecture}: {percentage}%")
    
    return top_3_architectures

def analyze_task_categories_bias_detection(df):
    """
    Analyze which task categories have the highest bias detection scores
    This function teaches median calculations and statistical analysis
    """
    print("\n=== STEP 5: Analyzing Task Categories Bias Detection Scores ===")
    
    # Group by task_category to analyze bias detection for each task type
    task_groups = df.groupby('task_category')
    print(f"✓ Found {len(task_groups)} different task categories")
    
    # Calculate median bias detection score for each task category
    # Median is the middle value - better than average for skewed data
    bias_medians = {}
    
    for task_category, group_data in task_groups:
        # Calculate median bias detection score
        median_score = group_data['bias_detection_score'].median()
        bias_medians[task_category] = round(median_score, 1)
        
        # Show some statistics for learning
        count = len(group_data)
        min_score = group_data['bias_detection_score'].min()
        max_score = group_data['bias_detection_score'].max()
        
        print(f"  {task_category}: median={median_score:.1f} (count={count}, range={min_score:.1f}-{max_score:.1f})")
    
    # Sort by median score (highest first) and get top 3
    sorted_results = sorted(bias_medians.items(), key=lambda x: x[1], reverse=True)
    top_3_task_categories = sorted_results[:3]
    
    print("\n✓ Top 3 Task Categories by Bias Detection Median Score:")
    for i, (task_category, median_score) in enumerate(top_3_task_categories, 1):
        print(f"  {i}. {task_category}: {median_score}")
    
    return top_3_task_categories

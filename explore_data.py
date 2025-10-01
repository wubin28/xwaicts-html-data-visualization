import pandas as pd

# Read Excel file
df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')

# Use first row as column headers
df.columns = df.iloc[0]
df = df.drop(df.index[0])

print('Dataset shape after fixing headers:', df.shape)
print('Columns:', list(df.columns))
print('First 5 rows:')
print(df.head())

# Check specific columns we need
required_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 'task_category', 'bias_detection']
available_columns = [col for col in required_columns if col in df.columns]
print('Required columns found:', available_columns)
print('Missing columns:', [col for col in required_columns if col not in df.columns])

# Check unique values in key columns
if 'agent_type' in df.columns:
    print('Unique agent types:', df['agent_type'].unique())
if 'multimodal_capability' in df.columns:
    print('Multimodal capability values:', df['multimodal_capability'].unique())
if 'model_architecture' in df.columns:
    print('Unique model architectures:', df['model_architecture'].unique())
if 'task_category' in df.columns:
    print('Unique task categories:', df['task_category'].unique())
if 'bias_detection' in df.columns:
    print('Bias detection sample values:', df['bias_detection'].head(10).tolist())
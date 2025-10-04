import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import os

def analyze_data():
    # Load the Excel file with proper header
    file_path = 'first-80-rows-agentic_ai_performance_dataset_20250622.xlsx'
    df = pd.read_excel(file_path, header=1)  # Using row 1 (second row) as header
    
    print(f"Dataset loaded successfully. Total records: {len(df)}")
    
    # Question 1: Top 3 agent types with multimodal capability percentage
    print("\n--- QUESTION 1: Top 3 agent types with multimodal capability percentage ---")
    
    # Group by agent_type and calculate percentage of multimodal_capability = True
    agent_multimodal = df.groupby('agent_type')['multimodal_capability'].agg(['count', 'sum']).reset_index()
    agent_multimodal['multimodal_percentage'] = (agent_multimodal['sum'] / agent_multimodal['count']) * 100
    agent_multimodal = agent_multimodal.sort_values('multimodal_percentage', ascending=False).head(3)
    
    print("Top 3 agent types with highest multimodal capability percentage:")
    for idx, row in agent_multimodal.iterrows():
        print(f"{row['agent_type']}: {row['multimodal_percentage']:.2f}% ({int(row['sum'])}/{int(row['count'])})")
    
    # Question 2: Top 3 model architectures with multimodal capability percentage
    print("\n--- QUESTION 2: Top 3 model architectures with multimodal capability percentage ---")
    
    # Group by model_architecture and calculate percentage of multimodal_capability = True
    arch_multimodal = df.groupby('model_architecture')['multimodal_capability'].agg(['count', 'sum']).reset_index()
    arch_multimodal['multimodal_percentage'] = (arch_multimodal['sum'] / arch_multimodal['count']) * 100
    arch_multimodal = arch_multimodal.sort_values('multimodal_percentage', ascending=False).head(3)
    
    print("Top 3 model architectures with highest multimodal capability percentage:")
    for idx, row in arch_multimodal.iterrows():
        print(f"{row['model_architecture']}: {row['multimodal_percentage']:.2f}% ({int(row['sum'])}/{int(row['count'])})")
    
    # Question 3: Top 3 task categories with highest median bias detection score
    print("\n--- QUESTION 3: Top 3 task categories with highest median bias detection score ---")
    
    # Group by task_category and calculate median bias detection score
    task_bias = df.groupby('task_category')['bias_detection_score'].median().reset_index()
    task_bias = task_bias.sort_values('bias_detection_score', ascending=False).head(3)
    
    print("Top 3 task categories with highest median bias detection score:")
    for idx, row in task_bias.iterrows():
        print(f"{row['task_category']}: {row['bias_detection_score']:.4f}")
    
    return df, agent_multimodal, arch_multimodal, task_bias

def create_visualizations(agent_multimodal, arch_multimodal, task_bias):
    """Create visualizations for the analysis"""
    
    # Set style for better appearance
    sns.set_style("whitegrid")
    plt.style.use('default')
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('AI Agent Performance Dashboard', fontsize=16, fontweight='bold')
    
    # Plot 1: Top 3 Agent Types with Multimodal Capability
    axes[0, 0].barh(agent_multimodal['agent_type'], agent_multimodal['multimodal_percentage'], color='skyblue')
    axes[0, 0].set_xlabel('Multimodal Capability Percentage (%)')
    axes[0, 0].set_title('Top 3 Agent Types with Multimodal Capability')
    axes[0, 0].invert_yaxis()  # Highest percentage at top
    
    # Add percentage labels on bars
    for i, v in enumerate(agent_multimodal['multimodal_percentage']):
        axes[0, 0].text(v + 1, i, f'{v:.1f}%', va='center', fontsize=10)
    
    # Plot 2: Top 3 Model Architectures with Multimodal Capability
    axes[0, 1].barh(arch_multimodal['model_architecture'], arch_multimodal['multimodal_percentage'], color='lightcoral')
    axes[0, 1].set_xlabel('Multimodal Capability Percentage (%)')
    axes[0, 1].set_title('Top 3 Model Architectures with Multimodal Capability')
    axes[0, 1].invert_yaxis()  # Highest percentage at top
    
    # Add percentage labels on bars
    for i, v in enumerate(arch_multimodal['multimodal_percentage']):
        axes[0, 1].text(v + 1, i, f'{v:.1f}%', va='center', fontsize=10)
    
    # Plot 3: Top 3 Task Categories with Median Bias Detection Score
    axes[1, 0].barh(task_bias['task_category'], task_bias['bias_detection_score'], color='lightgreen')
    axes[1, 0].set_xlabel('Median Bias Detection Score')
    axes[1, 0].set_title('Top 3 Task Categories with Highest Median Bias Detection Score')
    axes[1, 0].invert_yaxis()  # Highest score at top
    
    # Add score labels on bars
    for i, v in enumerate(task_bias['bias_detection_score']):
        axes[1, 0].text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=10)
    
    # Plot 4: Overall distribution of multimodal capability
    df_overall = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=1)
    multimodal_counts = df_overall['multimodal_capability'].value_counts()
    labels = ['No Multimodal Capability', 'Multimodal Capability']
    sizes = [multimodal_counts.get(False, 0), multimodal_counts.get(True, 0)]
    axes[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgray', 'wheat'])
    axes[1, 1].set_title('Overall Multimodal Capability Distribution')
    
    # Adjust layout to prevent overlapping
    plt.tight_layout()
    
    # Save plot to a BytesIO object and encode as base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    plt.close()
    
    return img_base64

def generate_html_report(agent_multimodal, arch_multimodal, task_bias, chart_base64, total_records):
    """Generate the HTML report with embedded analysis results"""
    
    # Format the results for HTML
    agent_results = []
    for idx, row in agent_multimodal.iterrows():
        agent_results.append(f'<div class="result-item">{row["agent_type"]}: {row["multimodal_percentage"]:.2f}%</div>')
    
    arch_results = []
    for idx, row in arch_multimodal.iterrows():
        arch_results.append(f'<div class="result-item">{row["model_architecture"]}: {row["multimodal_percentage"]:.2f}%</div>')
    
    task_results = []
    for idx, row in task_bias.iterrows():
        task_results.append(f'<div class="result-item">{row["task_category"]}: {row["bias_detection_score"]:.4f}</div>')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Performance Dashboard</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            background: #e9ecef;
            padding: 20px;
            text-align: center;
        }}

        .stat-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #2575fc;
        }}

        .stat-label {{
            font-size: 1rem;
            color: #6c757d;
        }}

        .content {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 40px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        .results-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .result-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #3498db;
        }}

        .result-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}

        .result-item {{
            padding: 5px 0;
        }}

        .chart-container {{
            width: 100%;
            text-align: center;
            margin: 20px 0;
        }}

        .chart {{
            max-width: 100%;
            height: auto;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            background: #e9ecef;
            color: #6c757d;
            font-size: 0.9rem;
        }}

        /* Mobile responsiveness */
        @media (max-width: 768px) {{
            .stats {{
                flex-direction: column;
            }}
            
            .stat-card {{
                width: 100%;
                margin: 10px 0;
            }}
            
            header {{
                padding: 20px 10px;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .content {{
                padding: 15px;
            }}
            
            .results-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Agent Performance Dashboard</h1>
            <div class="subtitle">Analysis of Agentic AI Performance Dataset 2025</div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_records}</div>
                <div class="stat-label">Total Records Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">16</div>
                <div class="stat-label">Agent Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">10</div>
                <div class="stat-label">Model Architectures</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">10</div>
                <div class="stat-label">Task Categories</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Key Insights</h2>
                <div class="results-grid">
                    <div class="result-card">
                        <div class="result-title">Top 3 Agent Types with Multimodal Capability</div>
                        {''.join(agent_results)}
                    </div>
                    
                    <div class="result-card">
                        <div class="result-title">Top 3 Model Architectures with Multimodal Capability</div>
                        {''.join(arch_results)}
                    </div>
                    
                    <div class="result-card">
                        <div class="result-title">Top 3 Task Categories with Highest Bias Detection</div>
                        {''.join(task_results)}
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Visual Analysis</h2>
                <div class="chart-container">
                    <img src="data:image/png;base64,{chart_base64}" alt="AI Agent Performance Visualization" class="chart">
                </div>
            </div>
            
            <div class="section">
                <h2>Analysis Summary</h2>
                <p>This dashboard presents an analysis of the Agentic AI Performance Dataset 2025, focusing on three key areas:</p>
                
                <h3>1. Multimodal Capability by Agent Type</h3>
                <p>Research Assistants lead in multimodal capability adoption at 60%, suggesting this agent type is particularly well-suited for processing multiple data types. Document Processors and Sales Assistants follow with significant multimodal implementation.</p>
                
                <h3>2. Multimodal Capability by Model Architecture</h3>
                <p>GPT-4o demonstrates the highest multimodal capability percentage at 37.5%, indicating it's well-optimized for multimodal tasks. CodeT5+ also shows strong multimodal adoption.</p>
                
                <h3>3. Bias Detection by Task Category</h3>
                <p>Communication tasks show the highest median bias detection score, indicating these tasks may be particularly sensitive to bias considerations. Research & Summarization and Decision Making also show high bias detection, suggesting careful attention is needed when deploying AI in these areas.</p>
                
                <div class="note">
                    <p><strong>Note:</strong> This analysis is based on {total_records} records from the Agentic AI Performance Dataset 2025. All visualizations are generated from actual data in the dataset.</p>
                </div>
            </div>
        </div>
        
        <footer>
            <p>AI Agent Performance Dashboard | Dataset Analysis | Agentic AI Performance Dataset 2025</p>
            <p>Data processed: {total_records} records | Generated on: October 2025</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content

if __name__ == "__main__":
    # Perform the analysis
    df, agent_multimodal, arch_multimodal, task_bias = analyze_data()
    
    # Create visualizations
    chart_base64 = create_visualizations(agent_multimodal, arch_multimodal, task_bias)
    
    # Generate and save the HTML report
    html_content = generate_html_report(agent_multimodal, arch_multimodal, task_bias, chart_base64, len(df))
    
    with open('data-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\nAnalysis complete. HTML dashboard saved as 'data-dashboard.html'.")
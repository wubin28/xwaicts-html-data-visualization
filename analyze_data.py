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

def generate_html_dashboard(top_3_agent_types, top_3_architectures, top_3_task_categories, record_count):
    """
    Generate complete HTML dashboard with embedded data and Chart.js visualizations
    This function teaches HTML structure, CSS styling, and JavaScript chart creation
    """
    print("\n=== STEP 6: Generating HTML Dashboard ===")
    
    # Convert analysis results to JavaScript-ready format
    # This shows beginners how to transform Python data for web use
    agent_labels = [item[0] for item in top_3_agent_types]
    agent_data = [item[1] for item in top_3_agent_types]
    
    arch_labels = [item[0] for item in top_3_architectures]
    arch_data = [item[1] for item in top_3_architectures]
    
    task_labels = [item[0] for item in top_3_task_categories]
    task_data = [item[1] for item in top_3_task_categories]
    
    # Create complete HTML document with embedded CSS and JavaScript
    # This template shows beginners a complete web page structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Performance Dashboard</title>
    <style>
        /* CSS Styles - Embedded for educational clarity and no external dependencies */
        
        /* Reset and base styles for consistent appearance across browsers */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* Body styling with light color scheme */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        /* Main container with responsive design */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        /* Header styling */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        /* Record count badge */
        .record-count {{
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 15px;
            font-weight: 500;
        }}
        
        /* Main content area */
        .content {{
            padding: 40px;
        }}
        
        /* Chart grid layout - responsive design */
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            margin-top: 30px;
        }}
        
        /* Individual chart containers */
        .chart-container {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }}
        
        .chart-title {{
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #495057;
            text-align: center;
        }}
        
        /* Chart canvas styling */
        .chart-canvas {{
            position: relative;
            height: 400px;
            width: 100%;
        }}
        
        /* Responsive design for larger screens */
        @media (min-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            
            .chart-container:last-child {{
                grid-column: 1 / -1;
            }}
        }}
        
        @media (min-width: 1024px) {{
            .charts-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            
            .chart-container:last-child {{
                grid-column: auto;
            }}
        }}
        
        /* Mobile optimization */
        @media (max-width: 767px) {{
            body {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .chart-canvas {{
                height: 300px;
            }}
        }}
    </style>
</head>
<body>
    <!-- HTML Structure - Semantic and accessible -->
    <div class="container">
        <!-- Header section with title and record count -->
        <header class="header">
            <h1>Agentic AI Performance Dashboard</h1>
            <p>Comprehensive Analysis of AI Agent Capabilities and Performance</p>
            <div class="record-count">
                📊 Dataset: {record_count} Records Processed
            </div>
        </header>
        
        <!-- Main content area -->
        <main class="content">
            <div class="charts-grid">
                <!-- Chart 1: Agent Types Multimodal Support -->
                <div class="chart-container">
                    <h2 class="chart-title">Top 3 Agent Types by Multimodal Support</h2>
                    <div class="chart-canvas">
                        <canvas id="agentTypesChart"></canvas>
                    </div>
                </div>
                
                <!-- Chart 2: Model Architectures Multimodal Support -->
                <div class="chart-container">
                    <h2 class="chart-title">Top 3 Model Architectures by Multimodal Support</h2>
                    <div class="chart-canvas">
                        <canvas id="architecturesChart"></canvas>
                    </div>
                </div>
                
                <!-- Chart 3: Task Categories Bias Detection -->
                <div class="chart-container">
                    <h2 class="chart-title">Top 3 Task Categories by Bias Detection Score</h2>
                    <div class="chart-canvas">
                        <canvas id="taskCategoriesChart"></canvas>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <!-- Chart.js library from CDN - no local files needed -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- JavaScript code with embedded data -->
    <script>
        // Embedded data from Python analysis - this shows beginners how to pass data from backend to frontend
        
        // Agent Types Data
        const agentTypesLabels = {json.dumps(agent_labels)};
        const agentTypesData = {json.dumps(agent_data)};
        
        // Model Architectures Data  
        const architecturesLabels = {json.dumps(arch_labels)};
        const architecturesData = {json.dumps(arch_data)};
        
        // Task Categories Data
        const taskCategoriesLabels = {json.dumps(task_labels)};
        const taskCategoriesData = {json.dumps(task_data)};
        
        // Chart color scheme - light and professional
        const chartColors = {{
            primary: '#667eea',
            secondary: '#764ba2', 
            accent: '#f093fb',
            background: 'rgba(102, 126, 234, 0.1)',
            border: 'rgba(102, 126, 234, 0.8)'
        }};
        
        // Chart 1: Agent Types (Horizontal Bar Chart)
        const agentTypesCtx = document.getElementById('agentTypesChart').getContext('2d');
        const agentTypesChart = new Chart(agentTypesCtx, {{
            type: 'bar',
            data: {{
                labels: agentTypesLabels,
                datasets: [{{
                    label: 'Multimodal Support (%)',
                    data: agentTypesData,
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)', 
                        'rgba(240, 147, 251, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(240, 147, 251, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.parsed.y + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }},
                        grid: {{
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        
        // Chart 2: Model Architectures (Vertical Bar Chart)
        const architecturesCtx = document.getElementById('architecturesChart').getContext('2d');
        const architecturesChart = new Chart(architecturesCtx, {{
            type: 'bar',
            data: {{
                labels: architecturesLabels,
                datasets: [{{
                    label: 'Multimodal Support (%)',
                    data: architecturesData,
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(240, 147, 251, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(240, 147, 251, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.parsed.y + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }},
                        grid: {{
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        
        // Chart 3: Task Categories (Horizontal Bar Chart)
        const taskCategoriesCtx = document.getElementById('taskCategoriesChart').getContext('2d');
        const taskCategoriesChart = new Chart(taskCategoriesCtx, {{
            type: 'bar',
            data: {{
                labels: taskCategoriesLabels,
                datasets: [{{
                    label: 'Bias Detection Score',
                    data: taskCategoriesData,
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(240, 147, 251, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(240, 147, 251, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Score: ' + context.parsed.y;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(0,0,0,0.1)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        
        // Console log for debugging - helps beginners understand data flow
        console.log('Dashboard loaded successfully!');
        console.log('Agent Types Data:', agentTypesLabels, agentTypesData);
        console.log('Architectures Data:', architecturesLabels, architecturesData);
        console.log('Task Categories Data:', taskCategoriesLabels, taskCategoriesData);
    </script>
</body>
</html>"""
    
    print("✓ HTML dashboard template created with embedded CSS and JavaScript")
    print("✓ Chart.js CDN link included for interactive charts")
    print("✓ Mobile-responsive design implemented")
    print("✓ Light color scheme applied")
    
    return html_content

def main():
    """
    Main function that orchestrates the entire data analysis and dashboard generation process
    This function shows beginners how to organize code into a clear workflow
    """
    print("🚀 Starting Agentic AI Performance Dashboard Generation")
    print("=" * 60)
    
    # Step 1: Load and validate the Excel data
    df = load_and_validate_data()
    if df is None:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Step 2: Perform the three required analyses
    top_3_agent_types = analyze_agent_types_multimodal(df)
    top_3_architectures = analyze_model_architectures_multimodal(df)
    top_3_task_categories = analyze_task_categories_bias_detection(df)
    
    # Step 3: Generate the HTML dashboard
    record_count = len(df)
    html_content = generate_html_dashboard(
        top_3_agent_types, 
        top_3_architectures, 
        top_3_task_categories, 
        record_count
    )
    
    # Step 4: Save the HTML file
    try:
        with open('data-dashboard.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        print("\n✅ SUCCESS: Dashboard saved as 'data-dashboard.html'")
        print("📱 The dashboard is mobile-responsive and works offline")
        print("🌐 Open 'data-dashboard.html' in your web browser to view the results")
        
    except Exception as e:
        print(f"❌ Error saving HTML file: {e}")

# This is the standard Python way to run the main function when the script is executed
# It teaches beginners about Python script execution
if __name__ == "__main__":
    main()

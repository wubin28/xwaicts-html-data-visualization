#!/usr/bin/env python3
"""
Data Analysis Script for Agentic AI Performance Dataset
Reads Excel file and generates HTML dashboard with visualizations.
"""

import pandas as pd
import json
import os
from datetime import datetime

class AgenticAIDataAnalyzer:
    """Analyzes Agentic AI Performance Dataset and generates dashboard."""
    
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.df = None
        self.total_records = 0
        
    def load_data(self):
        """Load and clean the Excel data."""
        try:
            # Read Excel with header=1 (second row contains column names)
            self.df = pd.read_excel(self.excel_file_path, header=1)
            self.total_records = len(self.df)
            print(f"Successfully loaded {self.total_records} records")
            return True
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return False
    
    def analyze_question1(self):
        """Analyze question 1: Top 3 agent types by multimodal capability proportion."""
        if self.df is None:
            return None
            
        # Group by agent_type and calculate multimodal capability proportion
        agent_type_analysis = self.df.groupby('agent_type')['multimodal_capability'].agg([
            ('total_count', 'count'),
            ('multimodal_true', lambda x: (x == True).sum() if 'multimodal_capability' in self.df.columns else 0),
            ('multimodal_false', lambda x: (x == False).sum() if 'multimodal_capability' in self.df.columns else 0)
        ]).reset_index()
        
        # Calculate proportion
        agent_type_analysis['multimodal_proportion'] = (
            agent_type_analysis['multimodal_true'] / agent_type_analysis['total_count']
        )
        
        # Get top 3 by proportion
        top_3_agent_types = agent_type_analysis.nlargest(3, 'multimodal_proportion')
        
        return top_3_agent_types.to_dict('records')
    
    def analyze_question2(self):
        """Analyze question 2: Top 3 model architectures by multimodal capability proportion."""
        if self.df is None:
            return None
            
        # Group by model_architecture and calculate multimodal capability proportion
        model_analysis = self.df.groupby('model_architecture')['multimodal_capability'].agg([
            ('total_count', 'count'),
            ('multimodal_true', lambda x: (x == True).sum() if 'multimodal_capability' in self.df.columns else 0),
            ('multimodal_false', lambda x: (x == False).sum() if 'multimodal_capability' in self.df.columns else 0)
        ]).reset_index()
        
        # Calculate proportion
        model_analysis['multimodal_proportion'] = (
            model_analysis['multimodal_true'] / model_analysis['total_count']
        )
        
        # Get top 3 by proportion
        top_3_models = model_analysis.nlargest(3, 'multimodal_proportion')
        
        return top_3_models.to_dict('records')
    
    def analyze_question3(self):
        """Analyze question 3: Top 3 task categories by median bias detection score."""
        if self.df is None:
            return None
            
        # Group by task_category and calculate median bias detection score
        task_analysis = self.df.groupby('task_category')['bias_detection_score'].agg([
            ('total_count', 'count'),
            ('median_score', 'median'),
            ('mean_score', 'mean'),
            ('min_score', 'min'),
            ('max_score', 'max')
        ]).reset_index()
        
        # Get top 3 by median score
        top_3_tasks = task_analysis.nlargest(3, 'median_score')
        
        return top_3_tasks.to_dict('records')
    
    def generate_chartjs_data(self):
        """Generate data in Chart.js format for HTML dashboard."""
        
        q1_results = self.analyze_question1()
        q2_results = self.analyze_question2()
        q3_results = self.analyze_question3()
        
        chart_data = {
            'total_records': self.total_records,
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'question1': q1_results,
            'question2': q2_results,
            'question3': q3_results
        }
        
        return chart_data
    
    def generate_html_dashboard(self, chart_data):
        """Generate HTML dashboard with embedded data and Chart.js visualizations."""
        
        # Convert data to JSON for embedding
        data_json = json.dumps(chart_data, indent=2)
        
        html_template = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI 性能数据看板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .stats-bar {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            border-left: 4px solid #2196f3;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
        }}
        
        .card h3 {{
            color: #2196f3;
            margin-bottom: 15px;
            border-bottom: 2px solid #e3f2fd;
            padding-bottom: 10px;
        }}
        
        .chart-container {{
            height: 300px;
            margin: 15px 0;
        }}
        
        .results-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .results-table th,
        .results-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        .results-table th {{
            background-color: #f5f5f5;
            font-weight: 600;
        }}
        
        .results-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        @media (max-width: 768px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic AI 性能数据看板</h1>
            <p>基于 Kaggle Agentic AI Performance Dataset 2025</p>
        </div>
        
        <div class="stats-bar">
            <strong>📊 数据处理统计:</strong> 成功读取并处理了 <span id="total-records">{chart_data['total_records']}</span> 条记录 | 
            <strong>⏰ 分析时间:</strong> <span id="analysis-time">{chart_data['analysis_timestamp']}</span>
        </div>
        
        <div class="dashboard-grid">
            <!-- 问题1: 智能体类型多模态能力占比 -->
            <div class="card">
                <h3>🔍 问题1: 多模态能力智能体类型排名</h3>
                <p><em>支持多模态处理的智能体类型占比排名前三</em></p>
                <div class="chart-container">
                    <canvas id="agentTypeChart"></canvas>
                </div>
                <table class="results-table" id="agentTypeResults">
                    <thead>
                        <tr>
                            <th>智能体类型</th>
                            <th>多模态能力占比</th>
                            <th>总数</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
            
            <!-- 问题2: 模型架构多模态能力占比 -->
            <div class="card">
                <h3>🏗️ 问题2: 多模态能力模型架构排名</h3>
                <p><em>支持多模态处理的大模型架构占比排名前三</em></p>
                <div class="chart-container">
                    <canvas id="modelArchitectureChart"></canvas>
                </div>
                <table class="results-table" id="modelArchitectureResults">
                    <thead>
                        <tr>
                            <th>模型架构</th>
                            <th>多模态能力占比</th>
                            <th>总数</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
            
            <!-- 问题3: 任务类别公正性评分 -->
            <div class="card">
                <h3>⚖️ 问题3: 任务类别公正性评分排名</h3>
                <p><em>各种智能体处理任务的公正性评分中位数排名前三</em></p>
                <div class="chart-container">
                    <canvas id="taskCategoryChart"></canvas>
                </div>
                <table class="results-table" id="taskCategoryResults">
                    <thead>
                        <tr>
                            <th>任务类别</th>
                            <th>公正性评分中位数</th>
                            <th>总数</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Embedded data from Python analysis
        const chartData = {data_json};
        
        // Light color palette for charts
        const lightColors = [
            'rgba(102, 126, 234, 0.8)',  // Light blue
            'rgba(118, 75, 162, 0.8)',   // Light purple
            'rgba(33, 150, 243, 0.8)',   // Light blue
            'rgba(76, 175, 80, 0.8)',    // Light green
            'rgba(255, 152, 0, 0.8)',    // Light orange
            'rgba(156, 39, 176, 0.8)'    // Light pink
        ];
        
        // Initialize charts
        function initializeCharts() {{
            // Question 1: Agent Type Multimodal Capability
            if (chartData.question1 && chartData.question1.length > 0) {{
                const agentTypes = chartData.question1.map(item => item.agent_type);
                const proportions = chartData.question1.map(item => (item.multimodal_proportion * 100).toFixed(1));
                
                // Create horizontal bar chart
                new Chart(document.getElementById('agentTypeChart'), {{
                    type: 'bar',
                    data: {{
                        labels: agentTypes,
                        datasets: [{{
                            label: '多模态能力占比 (%)',
                            data: proportions,
                            backgroundColor: lightColors.slice(0, agentTypes.length),
                            borderColor: lightColors.slice(0, agentTypes.length).map(color => color.replace('0.8', '1')),
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return `多模态能力占比: ${{context.parsed.x}}%`;
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{ display: true, text: '占比 (%)' }}
                            }},
                            y: {{
                                ticks: {{ font: {{ size: 12 }} }}
                            }}
                        }}
                    }}
                }});
                
                // Populate results table
                const tableBody = document.querySelector('#agentTypeResults tbody');
                chartData.question1.forEach(item => {{
                    const row = tableBody.insertRow();
                    row.innerHTML = `
                        <td>${{item.agent_type}}</td>
                        <td>${{(item.multimodal_proportion * 100).toFixed(1)}}%</td>
                        <td>${{item.total_count}}</td>
                    `;
                }});
            }}
            
            // Question 2: Model Architecture Multimodal Capability
            if (chartData.question2 && chartData.question2.length > 0) {{
                const models = chartData.question2.map(item => item.model_architecture);
                const proportions = chartData.question2.map(item => (item.multimodal_proportion * 100).toFixed(1));
                
                // Create horizontal bar chart
                new Chart(document.getElementById('modelArchitectureChart'), {{
                    type: 'bar',
                    data: {{
                        labels: models,
                        datasets: [{{
                            label: '多模态能力占比 (%)',
                            data: proportions,
                            backgroundColor: lightColors.slice(2, 2 + models.length),
                            borderColor: lightColors.slice(2, 2 + models.length).map(color => color.replace('0.8', '1')),
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return `多模态能力占比: ${{context.parsed.x}}%`;
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{ display: true, text: '占比 (%)' }}
                            }},
                            y: {{
                                ticks: {{ font: {{ size: 12 }} }}
                            }}
                        }}
                    }}
                }});
                
                // Populate results table
                const tableBody = document.querySelector('#modelArchitectureResults tbody');
                chartData.question2.forEach(item => {{
                    const row = tableBody.insertRow();
                    row.innerHTML = `
                        <td>${{item.model_architecture}}</td>
                        <td>${{(item.multimodal_proportion * 100).toFixed(1)}}%</td>
                        <td>${{item.total_count}}</td>
                    `;
                }});
            }}
            
            // Question 3: Task Category Bias Detection
            if (chartData.question3 && chartData.question3.length > 0) {{
                const tasks = chartData.question3.map(item => item.task_category);
                const medians = chartData.question3.map(item => item.median_score.toFixed(2));
                
                // Create horizontal bar chart
                new Chart(document.getElementById('taskCategoryChart'), {{
                    type: 'bar',
                    data: {{
                        labels: tasks,
                        datasets: [{{
                            label: '公正性评分中位数',
                            data: medians,
                            backgroundColor: lightColors.slice(4, 4 + tasks.length),
                            borderColor: lightColors.slice(4, 4 + tasks.length).map(color => color.replace('0.8', '1')),
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return `公正性评分中位数: ${{context.parsed.x}}`;
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                title: {{ display: true, text: '评分中位数' }}
                            }},
                            y: {{
                                ticks: {{ font: {{ size: 12 }} }}
                            }}
                        }}
                    }}
                }});
                
                // Populate results table
                const tableBody = document.querySelector('#taskCategoryResults tbody');
                chartData.question3.forEach(item => {{
                    const row = tableBody.insertRow();
                    row.innerHTML = `
                        <td>${{item.task_category}}</td>
                        <td>${{item.median_score.toFixed(2)}}</td>
                        <td>${{item.total_count}}</td>
                    `;
                }});
            }}
        }}
        
        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', initializeCharts);
    </script>
</body>
</html>
'''
        
        return html_template

    def run_analysis(self):
        """Run complete analysis and generate dashboard."""
        print("Starting Agentic AI Performance Data Analysis...")
        
        # Load data
        if not self.load_data():
            print("Failed to load data")
            return False
        
        # Generate chart data
        chart_data = self.generate_chartjs_data()
        
        # Generate HTML dashboard
        html_content = self.generate_html_dashboard(chart_data)
        
        # Save HTML file
        with open('data-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Processed {self.total_records} records")
        print(f"🌐 Dashboard saved as: data-dashboard.html")
        
        return True

def main():
    """Main function to run the analysis."""
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ Error: Excel file '{excel_file}' not found")
        return
    
    # Create analyzer and run analysis
    analyzer = AgenticAIDataAnalyzer(excel_file)
    success = analyzer.run_analysis()
    
    if success:
        print("\n🎉 Data dashboard generation completed!")
        print("📁 Files created:")
        print("   - read-excel-data.py (this script)")
        print("   - data-dashboard.html (interactive dashboard)")
        print("\n🔗 Open 'data-dashboard.html' in your browser to view the results.")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
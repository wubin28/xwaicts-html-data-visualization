import pandas as pd
import json

# 读取Excel数据，跳过第一行（文件名信息）
def read_excel_data(file_path):
    try:
        df = pd.read_excel(file_path, skiprows=1)
        print(f"成功读取数据，共{len(df)}条记录")
        return df
    except Exception as e:
        print(f"读取数据时发生错误：{e}")
        return None

# 分析问题1：支持多模态处理的智能体类型占比
def analyze_agent_type(df):
    # 筛选支持多模态处理的智能体
    multimodal_agents = df[df['multimodal_capability'] == 1]
    # 计算每种智能体类型的总数和支持多模态的数量
    total_by_type = df['agent_type'].value_counts()
    multimodal_by_type = multimodal_agents['agent_type'].value_counts()
    # 计算占比
    ratio_by_type = (multimodal_by_type / total_by_type * 100).dropna()
    # 返回排名前三的结果
    return ratio_by_type.sort_values(ascending=False).head(3)

# 分析问题2：支持多模态处理的大模型架构占比
def analyze_model_architecture(df):
    # 筛选支持多模态处理的模型
    multimodal_models = df[df['multimodal_capability'] == 1]
    # 计算每种架构的总数和支持多模态的数量
    total_by_arch = df['model_architecture'].value_counts()
    multimodal_by_arch = multimodal_models['model_architecture'].value_counts()
    # 计算占比
    ratio_by_arch = (multimodal_by_arch / total_by_arch * 100).dropna()
    # 返回排名前三的结果
    return ratio_by_arch.sort_values(ascending=False).head(3)

# 分析问题3：任务类别公正性中位数
def analyze_task_fairness(df):
    # 按任务类别分组，计算公正性分数的中位数
    median_fairness = df.groupby('task_category')['bias_detection_score'].median()
    # 返回排名前三的结果
    return median_fairness.sort_values(ascending=False).head(3)

# 将分析结果转换为可嵌入HTML的数据结构
def prepare_data_for_html(agent_type_result, model_arch_result, task_fairness_result, total_records):
    # 准备问题1的数据
    agent_type_data = {
        'labels': agent_type_result.index.tolist(),
        'values': agent_type_result.values.tolist()
    }
    
    # 准备问题2的数据
    model_arch_data = {
        'labels': model_arch_result.index.tolist(),
        'values': model_arch_result.values.tolist()
    }
    
    # 准备问题3的数据
    task_fairness_data = {
        'labels': task_fairness_result.index.tolist(),
        'values': task_fairness_result.values.tolist()
    }
    
    # 整合所有数据
    all_data = {
        'agent_type': agent_type_data,
        'model_architecture': model_arch_data,
        'task_fairness': task_fairness_data,
        'total_records': total_records
    }
    
    # 转换为JSON格式
    return json.dumps(all_data, ensure_ascii=False)

# 生成完整的HTML文件
def generate_html_dashboard(agent_type_result, model_arch_result, task_fairness_result, total_records):
    # 准备图表数据
    chart_data = prepare_data_for_html(agent_type_result, model_arch_result, task_fairness_result, total_records)
    
    # 获取当前日期
    current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    
    # HTML模板
    html_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI智能体性能数据分析看板</title>
    <style>
        /* 基础样式 */
        * {{\n            margin: 0;\n            padding: 0;\n            box-sizing: border-box;\n        }}
        
        body {{\n            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;\n            background-color: #f8f9fa;\n            color: #333;\n            line-height: 1.6;\n        }}
        
        .container {{\n            max-width: 1200px;\n            margin: 0 auto;\n            padding: 20px;\n        }}
        
        header {{\n            text-align: center;\n            margin-bottom: 30px;\n            padding: 20px;\n            background-color: #fff;\n            border-radius: 8px;\n            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);\n        }}
        
        h1 {{\n            font-size: 28px;\n            color: #2c3e50;\n            margin-bottom: 10px;\n        }}
        
        /* 统计摘要区域 */
        .summary {{\n            background-color: #fff;\n            padding: 20px;\n            border-radius: 8px;\n            margin-bottom: 30px;\n            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);\n        }}
        
        .summary p {{\n            font-size: 16px;\n            color: #666;\n        }}
        
        .summary strong {{\n            color: #2c3e50;\n        }}
        
        /* 图表容器样式 */
        .charts-container {{\n            display: grid;\n            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));\n            gap: 20px;\n            margin-bottom: 30px;\n        }}
        
        .chart-card {{\n            background-color: #fff;\n            padding: 20px;\n            border-radius: 8px;\n            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);\n        }}
        
        .chart-card h2 {{\n            font-size: 20px;\n            color: #2c3e50;\n            margin-bottom: 20px;\n            text-align: center;\n        }}
        
        .chart-container {{\n            height: 300px;\n            position: relative;\n        }}
        
        /* 页脚样式 */
        footer {{\n            text-align: center;\n            padding: 20px;\n            color: #666;\n            font-size: 14px;\n        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{\n            .charts-container {{\n                grid-template-columns: 1fr;\n            }}\n            \n            h1 {{\n                font-size: 24px;\n            }}\n            \n            .chart-card h2 {{\n                font-size: 18px;\n            }}\n        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面标题 -->
        <header>
            <h1>AI智能体性能数据分析看板</h1>
            <p>基于Agentic AI Performance Dataset 2025的分析结果</p>
        </header>
        
        <!-- 数据统计摘要 -->
        <div class="summary">
            <p><strong>总记录数：</strong><span id="total-records">{total_records}</span>条</p>
            <p><strong>分析时间：</strong><span id="analysis-time">{current_date}</span></p>
        </div>
        
        <!-- 图表容器 -->
        <div class="charts-container">
            <!-- 图表1：支持多模态处理的智能体类型占比 -->
            <div class="chart-card">
                <h2>支持多模态处理的智能体类型占比前三</h2>
                <div class="chart-container">
                    <canvas id="agentTypeChart"></canvas>
                </div>
            </div>
            
            <!-- 图表2：支持多模态处理的大模型架构占比 -->
            <div class="chart-card">
                <h2>支持多模态处理的大模型架构占比前三</h2>
                <div class="chart-container">
                    <canvas id="modelArchChart"></canvas>
                </div>
            </div>
            
            <!-- 图表3：任务类别公正性中位数 -->
            <div class="chart-card">
                <h2>任务类别公正性中位数前三</h2>
                <div class="chart-container">
                    <canvas id="taskFairnessChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- 页脚 -->
        <footer>
            <p>数据来源：Agentic AI Performance Dataset 2025 | 分析工具：Python & HTML</p>
        </footer>
    </div>
    
    <!-- Chart.js库 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- 数据可视化脚本 -->
    <script>
        // 图表数据
        const chartData = {chart_data};
        
        // 设置图表颜色主题
        const colors = {{
            background: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)'
            ],
            border: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ]
        }};
        
        // 创建智能体类型占比图表
        const agentTypeCtx = document.getElementById('agentTypeChart').getContext('2d');
        new Chart(agentTypeCtx, {{
            type: 'doughnut',
            data: {{
                labels: chartData.agent_type.labels,
                datasets: [{{
                    data: chartData.agent_type.values,
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return `${{context.label}}: ${{context.parsed.toFixed(2)}}%`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // 创建模型架构占比图表
        const modelArchCtx = document.getElementById('modelArchChart').getContext('2d');
        new Chart(modelArchCtx, {{
            type: 'doughnut',
            data: {{
                labels: chartData.model_architecture.labels,
                datasets: [{{
                    data: chartData.model_architecture.values,
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return `${{context.label}}: ${{context.parsed.toFixed(2)}}%`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // 创建任务公正性中位数图表
        const taskFairnessCtx = document.getElementById('taskFairnessChart').getContext('2d');
        new Chart(taskFairnessCtx, {{
            type: 'bar',
            data: {{
                labels: chartData.task_fairness.labels,
                datasets: [{{
                    label: '公正性中位数',
                    data: chartData.task_fairness.values,
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 1,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(2);
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return `公正性中位数: ${{context.parsed.y.toFixed(2)}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // 设置当前日期
        document.getElementById('analysis-time').textContent = new Date().toISOString().split('T')[0];
    </script>
</body>
</html>
    '''
    
    # 填充模板变量
    html_content = html_template.format(
        total_records=total_records,
        current_date=current_date,
        chart_data=chart_data
    )
    
    # 写入文件
    with open('data-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成HTML看板：data-dashboard.html")

# 如果直接运行此脚本，进行简单的测试
if __name__ == "__main__":
    file_path = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
    data = read_excel_data(file_path)
    if data is not None:
        # 显示数据的基本信息
        print("\n数据列名：")
        print(data.columns.tolist())
        print("\n前5行数据：")
        print(data.head())
        
        # 测试分析函数
        print("\n问题1：支持多模态处理的智能体类型占比前三：")
        agent_type_result = analyze_agent_type(data)
        print(agent_type_result)
        
        print("\n问题2：支持多模态处理的大模型架构占比前三：")
        model_arch_result = analyze_model_architecture(data)
        print(model_arch_result)
        
        print("\n问题3：任务类别公正性中位数前三：")
        task_fairness_result = analyze_task_fairness(data)
        print(task_fairness_result)
        
        # 测试数据转换函数
        print("\n准备HTML数据结构：")
        html_data = prepare_data_for_html(agent_type_result, model_arch_result, task_fairness_result, len(data))
        print(html_data)
        
        # 生成HTML看板
        print("\n生成HTML数据看板：")
        generate_html_dashboard(agent_type_result, model_arch_result, task_fairness_result, len(data))
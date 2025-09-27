#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取Excel数据并生成HTML数据看板
用于分析Agentic AI Performance Dataset 2025数据集
"""

import pandas as pd
import os

def read_excel_data():
    """
    读取Excel文件数据
    
    Returns:
        pandas.DataFrame: 包含所有数据的数据框
    """
    # Excel文件路径
    excel_file = 'first-80-rows-agentic_ai_performance_dataset_20250622.xlsx'
    
    # 检查文件是否存在
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel文件 {excel_file} 不存在")
    
    # 读取Excel数据，使用第二行作为列名（header=1）
    df = pd.read_excel(excel_file, header=1)
    
    # 打印数据基本信息
    print(f"成功读取数据，形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print(f"总记录数: {len(df)}")
    
    return df

def analyze_agent_type_multimodal(df):
    """
    分析问题1: 智能体类型多模态支持占比排名
    
    Args:
        df: 数据框
    
    Returns:
        pandas.Series: 按占比降序排列的智能体类型多模态支持率
    """
    # 按智能体类型分组，计算multimodal_capability的均值（占比）
    agent_type_stats = df.groupby('agent_type')['multimodal_capability'].mean()
    
    # 按占比降序排序
    agent_type_stats_sorted = agent_type_stats.sort_values(ascending=False)
    
    print("\n=== 问题1分析: 智能体类型多模态支持占比排名 ===")
    print("所有智能体类型的多模态支持率:")
    for agent_type, percentage in agent_type_stats_sorted.items():
        print(f"  {agent_type}: {percentage:.2%}")
    
    # 获取前三名
    top_3 = agent_type_stats_sorted.head(3)
    print("\n前三名:")
    for i, (agent_type, percentage) in enumerate(top_3.items(), 1):
        print(f"  第{i}名: {agent_type} - {percentage:.2%}")
    
    return agent_type_stats_sorted


def analyze_model_architecture_multimodal(df):
    """
    分析问题2: 模型架构多模态支持占比排名
    
    Args:
        df: 数据框
    
    Returns:
        pandas.Series: 按占比降序排列的模型架构多模态支持率
    """
    # 按模型架构分组，计算multimodal_capability的均值（占比）
    model_arch_stats = df.groupby('model_architecture')['multimodal_capability'].mean()
    
    # 按占比降序排序
    model_arch_stats_sorted = model_arch_stats.sort_values(ascending=False)
    
    print("\n=== 问题2分析: 模型架构多模态支持占比排名 ===")
    print("所有模型架构的多模态支持率:")
    for model_arch, percentage in model_arch_stats_sorted.items():
        print(f"  {model_arch}: {percentage:.2%}")
    
    # 获取前三名
    top_3 = model_arch_stats_sorted.head(3)
    print("\n前三名:")
    for i, (model_arch, percentage) in enumerate(top_3.items(), 1):
        print(f"  第{i}名: {model_arch} - {percentage:.2%}")
    
    return model_arch_stats_sorted


def analyze_task_category_bias_median(df):
    """
    分析问题3: 任务类别公正性中位数排名
    
    Args:
        df: 数据框
    
    Returns:
        pandas.Series: 按中位数降序排列的任务类别公正性分数
    """
    # 按任务类别分组，计算bias_detection_score的中位数
    task_category_stats = df.groupby('task_category')['bias_detection_score'].median()
    
    # 按中位数降序排序
    task_category_stats_sorted = task_category_stats.sort_values(ascending=False)
    
    print("\n=== 问题3分析: 任务类别公正性中位数排名 ===")
    print("所有任务类别的公正性中位数:")
    for task_category, median_score in task_category_stats_sorted.items():
        print(f"  {task_category}: {median_score:.6f}")
    
    # 获取前三名
    top_3 = task_category_stats_sorted.head(3)
    print("\n前三名:")
    for i, (task_category, median_score) in enumerate(top_3.items(), 1):
        print(f"  第{i}名: {task_category} - {median_score:.6f}")
    
    return task_category_stats_sorted


def generate_html_dashboard(df, agent_type_stats, model_arch_stats, task_category_stats):
    """
    生成HTML数据看板
    
    Args:
        df: 原始数据框
        agent_type_stats: 智能体类型分析结果
        model_arch_stats: 模型架构分析结果
        task_category_stats: 任务类别分析结果
    
    Returns:
        str: HTML内容字符串
    """
    # HTML头部和CSS样式
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Performance Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .overview {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .overview h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        
        .overview-item {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        
        .overview-item h3 {
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .overview-item p {
            color: #666;
            font-size: 0.9rem;
        }
        
        .section {
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .chart-container {
            margin-bottom: 25px;
        }
        
        .chart {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 30px;
            border-radius: 15px;
            margin: 10px 0;
            position: relative;
            overflow: hidden;
        }
        
        .chart-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            border-radius: 15px;
            transition: width 0.3s ease;
        }
        
        .chart-label {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        
        .chart-value {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        
        .table-container {
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        th {
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e9ecef;
        }
        
        .rank-1 { background-color: #fff3cd !important; }
        .rank-2 { background-color: #d1ecf1 !important; }
        .rank-3 { background-color: #d4edda !important; }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .overview-grid {
                grid-template-columns: 1fr;
            }
            
            .section {
                padding: 15px;
            }
            
            th, td {
                padding: 8px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic AI Performance Dashboard</h1>
            <p>基于Agentic AI Performance Dataset 2025的数据分析看板</p>
        </div>
        
        <div class="overview">
            <h2>📊 数据概览</h2>
            <div class="overview-grid">
                <div class="overview-item">
                    <h3>""" + str(len(df)) + """</h3>
                    <p>总记录数</p>
                </div>
                <div class="overview-item">
                    <h3>""" + str(df['agent_type'].nunique()) + """</h3>
                    <p>智能体类型</p>
                </div>
                <div class="overview-item">
                    <h3>""" + str(df['model_architecture'].nunique()) + """</h3>
                    <p>模型架构</p>
                </div>
                <div class="overview-item">
                    <h3>""" + str(df['task_category'].nunique()) + """</h3>
                    <p>任务类别</p>
                </div>
            </div>
        </div>
        """
    
    # 添加问题1分析部分
    html_content += """
        <div class="section">
            <h2>📈 问题1: 智能体类型多模态支持占比排名</h2>
            <div class="chart-container">
    """
    
    # 添加问题1的图表
    for i, (agent_type, percentage) in enumerate(agent_type_stats.items(), 1):
        html_content += f"""
                <div class="chart">
                    <div class="chart-fill" style="width: {percentage*100}%"></div>
                    <span class="chart-label">{agent_type}</span>
                    <span class="chart-value">{percentage:.2%}</span>
                </div>
        """
    
    html_content += """
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>智能体类型</th>
                            <th>多模态支持率</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # 添加问题1的表格
    for i, (agent_type, percentage) in enumerate(agent_type_stats.items(), 1):
        rank_class = f"rank-{i}" if i <= 3 else ""
        html_content += f"""
                        <tr class="{rank_class}">
                            <td>{i}</td>
                            <td>{agent_type}</td>
                            <td>{percentage:.2%}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    """
    
    # 添加问题2分析部分
    html_content += """
        <div class="section">
            <h2>📊 问题2: 模型架构多模态支持占比排名</h2>
            <div class="chart-container">
    """
    
    # 添加问题2的图表
    for i, (model_arch, percentage) in enumerate(model_arch_stats.items(), 1):
        html_content += f"""
                <div class="chart">
                    <div class="chart-fill" style="width: {percentage*100}%"></div>
                    <span class="chart-label">{model_arch}</span>
                    <span class="chart-value">{percentage:.2%}</span>
                </div>
        """
    
    html_content += """
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>模型架构</th>
                            <th>多模态支持率</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # 添加问题2的表格
    for i, (model_arch, percentage) in enumerate(model_arch_stats.items(), 1):
        rank_class = f"rank-{i}" if i <= 3 else ""
        html_content += f"""
                        <tr class="{rank_class}">
                            <td>{i}</td>
                            <td>{model_arch}</td>
                            <td>{percentage:.2%}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    """
    
    # 添加问题3分析部分
    html_content += """
        <div class="section">
            <h2>⚖️ 问题3: 任务类别公正性中位数排名</h2>
            <div class="chart-container">
    """
    
    # 添加问题3的图表
    max_score = task_category_stats.max()
    for i, (task_category, median_score) in enumerate(task_category_stats.items(), 1):
        width_percentage = (median_score / max_score) * 100
        html_content += f"""
                <div class="chart">
                    <div class="chart-fill" style="width: {width_percentage}%"></div>
                    <span class="chart-label">{task_category}</span>
                    <span class="chart-value">{median_score:.6f}</span>
                </div>
        """
    
    html_content += """
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>任务类别</th>
                            <th>公正性中位数</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # 添加问题3的表格
    for i, (task_category, median_score) in enumerate(task_category_stats.items(), 1):
        rank_class = f"rank-{i}" if i <= 3 else ""
        html_content += f"""
                        <tr class="{rank_class}">
                            <td>{i}</td>
                            <td>{task_category}</td>
                            <td>{median_score:.6f}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    """
    
    # 添加页脚
    html_content += """
        <div class="footer">
            <p>Generated on """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """ | Agentic AI Performance Analysis</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content


def main():
    """主函数"""
    try:
        # 读取数据
        df = read_excel_data()
        
        # 显示数据前几行
        print("\n前5行数据:")
        print(df.head())
        
        # 显示关键字段的基本信息
        print("\n关键字段信息:")
        print(f"multimodal_capability 唯一值: {df['multimodal_capability'].unique()}")
        print(f"agent_type 唯一值数量: {df['agent_type'].nunique()}")
        print(f"model_architecture 唯一值数量: {df['model_architecture'].nunique()}")
        print(f"task_category 唯一值数量: {df['task_category'].nunique()}")
        
        # 执行问题1分析
        agent_type_stats = analyze_agent_type_multimodal(df)
        
        # 执行问题2分析
        model_arch_stats = analyze_model_architecture_multimodal(df)
        
        # 执行问题3分析
        task_category_stats = analyze_task_category_bias_median(df)
        
        # 生成HTML看板
        html_content = generate_html_dashboard(df, agent_type_stats, model_arch_stats, task_category_stats)
        
        # 保存HTML文件
        with open('data-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ HTML数据看板已保存到: data-dashboard.html")
        
        return df, agent_type_stats, model_arch_stats, task_category_stats
        
    except Exception as e:
        print(f"错误: {e}")
        return None, None, None, None

if __name__ == "__main__":
    main()
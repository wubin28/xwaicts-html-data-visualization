#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能体性能数据集分析脚本
Agentic AI Performance Dataset Analysis Script

本脚本用于读取和分析AI智能体性能Excel数据集，执行三项主要分析：
1. 各智能体类型的多模态处理能力支持比例排名
2. 各大模型架构的多模态处理能力支持比例排名
3. 各任务类别的偏见检测得分中位数排名

This script reads and analyzes an AI agent performance Excel dataset, performing three main analyses:
1. Ranking agent types by multimodal capability support ratio
2. Ranking model architectures by multimodal capability support ratio
3. Ranking task categories by bias detection score median
"""

# 导入必要的库 / Import required libraries
import pandas as pd  # 用于数据处理和分析 / For data processing and analysis
import numpy as np   # 用于数值计算 / For numerical computations
import json         # 用于JSON数据格式处理 / For JSON data format handling

def read_dataset(file_path):
    """
    读取Excel数据集
    Read Excel dataset

    Args:
        file_path (str): Excel文件路径 / Excel file path

    Returns:
        pandas.DataFrame: 加载的数据集 / Loaded dataset
    """
    print("正在读取数据集... / Reading dataset...")

    # 使用pandas读取Excel文件，第二行作为列标题（header=1）
    # Read Excel file with pandas, using second row as column headers (header=1)
    df = pd.read_excel(file_path, header=1)

    print(f"数据集加载成功！Dataset loaded successfully!")
    print(f"数据形状 / Data shape: {df.shape[0]} 行/rows, {df.shape[1]} 列/columns")

    return df

def analyze_agent_type_multimodal(df):
    """
    分析1：计算各智能体类型的多模态处理能力支持比例
    Analysis 1: Calculate multimodal capability support ratio by agent type

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        pandas.DataFrame: 排序后的结果 / Sorted results
    """
    print("\n=== 分析1：智能体类型多模态支持比例 / Analysis 1: Agent Type Multimodal Support Ratio ===")

    # 按智能体类型分组，计算多模态支持的数量和总数
    # Group by agent type, calculate count of multimodal support and total count
    multimodal_stats = df.groupby('agent_type')['multimodal_capability'].agg([
        ('support_count', 'sum'),      # 支持多模态的数量 / Count of multimodal support
        ('total_count', 'count')       # 该类型的总数量 / Total count of this type
    ])

    # 计算支持比例 / Calculate support ratio
    multimodal_stats['support_ratio'] = multimodal_stats['support_count'] / multimodal_stats['total_count']

    # 按支持比例降序排序 / Sort by support ratio in descending order
    multimodal_stats = multimodal_stats.sort_values('support_ratio', ascending=False)

    # 显示前3名 / Display top 3
    print("前3名智能体类型 / Top 3 agent types:")
    for i, (agent_type, stats) in enumerate(multimodal_stats.head(3).iterrows(), 1):
        ratio = stats['support_ratio']
        support = int(stats['support_count'])
        total = int(stats['total_count'])
        print(f"{i}. {agent_type}: {ratio:.3f} ({support}/{total})")

    return multimodal_stats.head(3)

def analyze_model_architecture_multimodal(df):
    """
    分析2：计算各大模型架构的多模态处理能力支持比例
    Analysis 2: Calculate multimodal capability support ratio by model architecture

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        pandas.DataFrame: 排序后的结果 / Sorted results
    """
    print("\n=== 分析2：大模型架构多模态支持比例 / Analysis 2: Model Architecture Multimodal Support Ratio ===")

    # 按模型架构分组，计算多模态支持的数量和总数
    # Group by model architecture, calculate count of multimodal support and total count
    multimodal_stats = df.groupby('model_architecture')['multimodal_capability'].agg([
        ('support_count', 'sum'),      # 支持多模态的数量 / Count of multimodal support
        ('total_count', 'count')       # 该架构的总数量 / Total count of this architecture
    ])

    # 计算支持比例 / Calculate support ratio
    multimodal_stats['support_ratio'] = multimodal_stats['support_count'] / multimodal_stats['total_count']

    # 按支持比例降序排序 / Sort by support ratio in descending order
    multimodal_stats = multimodal_stats.sort_values('support_ratio', ascending=False)

    # 显示前3名 / Display top 3
    print("前3名大模型架构 / Top 3 model architectures:")
    for i, (architecture, stats) in enumerate(multimodal_stats.head(3).iterrows(), 1):
        ratio = stats['support_ratio']
        support = int(stats['support_count'])
        total = int(stats['total_count'])
        print(f"{i}. {architecture}: {ratio:.3f} ({support}/{total})")

    return multimodal_stats.head(3)

def analyze_task_category_bias_detection(df):
    """
    分析3：计算各任务类别的偏见检测得分中位数
    Analysis 3: Calculate bias detection score median by task category

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        pandas.DataFrame: 排序后的结果 / Sorted results
    """
    print("\n=== 分析3：任务类别偏见检测得分中位数 / Analysis 3: Task Category Bias Detection Score Median ===")

    # 按任务类别分组，计算偏见检测得分的中位数和样本数量
    # Group by task category, calculate median of bias detection score and sample count
    bias_stats = df.groupby('task_category')['bias_detection_score'].agg([
        ('median_score', 'median'),    # 中位数得分 / Median score
        ('sample_count', 'count')      # 样本数量 / Sample count
    ])

    # 按中位数得分降序排序 / Sort by median score in descending order
    bias_stats = bias_stats.sort_values('median_score', ascending=False)

    # 显示前3名 / Display top 3
    print("前3名任务类别 / Top 3 task categories:")
    for i, (task_category, stats) in enumerate(bias_stats.head(3).iterrows(), 1):
        median = stats['median_score']
        count = int(stats['sample_count'])
        print(f"{i}. {task_category}: {median:.3f} (n={count})")

    return bias_stats.head(3)

def generate_javascript_data(agent_results, model_results, task_results, total_rows):
    """
    生成JavaScript格式的数据数组，用于HTML页面
    Generate JavaScript format data arrays for HTML page

    Args:
        agent_results: 智能体类型分析结果 / Agent type analysis results
        model_results: 模型架构分析结果 / Model architecture analysis results
        task_results: 任务类别分析结果 / Task category analysis results
        total_rows: 总数据行数 / Total number of data rows

    Returns:
        str: JavaScript代码字符串 / JavaScript code string
    """
    print("\n正在生成JavaScript数据格式... / Generating JavaScript data format...")

    # 转换智能体类型数据 / Convert agent type data
    agent_data = []
    for agent_type, stats in agent_results.iterrows():
        agent_data.append({
            'name': agent_type,
            'ratio': round(stats['support_ratio'], 3),
            'support_count': int(stats['support_count']),
            'total_count': int(stats['total_count'])
        })

    # 转换模型架构数据 / Convert model architecture data
    model_data = []
    for architecture, stats in model_results.iterrows():
        model_data.append({
            'name': architecture,
            'ratio': round(stats['support_ratio'], 3),
            'support_count': int(stats['support_count']),
            'total_count': int(stats['total_count'])
        })

    # 转换任务类别数据 / Convert task category data
    task_data = []
    for task_category, stats in task_results.iterrows():
        task_data.append({
            'name': task_category,
            'median_score': round(stats['median_score'], 3),
            'sample_count': int(stats['sample_count'])
        })

    # 生成JavaScript代码 / Generate JavaScript code
    js_code = f"""
// AI智能体性能数据分析结果 / AI Agent Performance Data Analysis Results
// 数据处理日期 / Data processed date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
// 总数据行数 / Total data rows: {total_rows}

// 分析1：智能体类型多模态支持比例前3名 / Analysis 1: Top 3 Agent Types by Multimodal Support Ratio
const agentTypeData = {json.dumps(agent_data, indent=2, ensure_ascii=False)};

// 分析2：大模型架构多模态支持比例前3名 / Analysis 2: Top 3 Model Architectures by Multimodal Support Ratio
const modelArchitectureData = {json.dumps(model_data, indent=2, ensure_ascii=False)};

// 分析3：任务类别偏见检测得分中位数前3名 / Analysis 3: Top 3 Task Categories by Bias Detection Score Median
const taskCategoryData = {json.dumps(task_data, indent=2, ensure_ascii=False)};

// 数据集信息 / Dataset Information
const datasetInfo = {{
    totalRows: {total_rows},
    analysisDate: "{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
}};
"""

    return js_code

def main():
    """
    主函数：执行完整的数据分析流程
    Main function: Execute complete data analysis workflow
    """
    print("开始AI智能体性能数据分析 / Starting AI Agent Performance Data Analysis")
    print("=" * 60)

    try:
        # 1. 读取数据集 / Read dataset
        df = read_dataset('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')

        # 2. 执行三项分析 / Perform three analyses
        agent_results = analyze_agent_type_multimodal(df)
        model_results = analyze_model_architecture_multimodal(df)
        task_results = analyze_task_category_bias_detection(df)

        # 3. 生成JavaScript数据 / Generate JavaScript data
        js_data = generate_javascript_data(agent_results, model_results, task_results, len(df))

        # 4. 输出JavaScript数据到控制台（用于复制到HTML文件）
        # Output JavaScript data to console (for copying to HTML file)
        print("\n" + "=" * 60)
        print("JavaScript数据输出 / JavaScript Data Output:")
        print("请将以下代码复制到HTML文件中 / Please copy the following code to HTML file:")
        print("=" * 60)
        print(js_data)

        # 5. 将JavaScript数据保存到文件
        # Save JavaScript data to file
        with open('dashboard-data.js', 'w', encoding='utf-8') as f:
            f.write(js_data)
        print(f"\nJavaScript数据已保存到 dashboard-data.js / JavaScript data saved to dashboard-data.js")

        print(f"\n数据分析完成！Data analysis completed!")
        print(f"实际处理的数据行数 / Actual data rows processed: {len(df)}")

    except Exception as e:
        print(f"错误 / Error: {str(e)}")
        print("请确保Excel文件存在且格式正确 / Please ensure Excel file exists and format is correct")

# 当直接运行此脚本时执行主函数 / Execute main function when running this script directly
if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能体性能数据分析脚本
阶段1: 基础入门方案

功能:
1. 读取Excel数据文件
2. 分析三个研究问题
3. 生成可视化图表
4. 创建HTML数据看板

作者: 学习者
创建时间: 2025-09-30
"""

import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def load_data():
    """读取Excel文件并验证数据"""
    try:
        # 读取Excel文件，使用第二行作为列名
        df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=1)

        # 验证数据
        print(f"✅ 成功读取数据，形状: {df.shape}")

        # 检查是否有80行数据
        if len(df) != 80:
            print(f"⚠️ 警告: 预期80行数据，实际读取{len(df)}行")

        # 检查关键列是否存在
        required_columns = ['agent_type', 'model_architecture', 'task_category',
                          'multimodal_capability', 'bias_detection_score']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"缺少必要的列: {missing_columns}")

        print("✅ 数据验证通过")
        return df

    except FileNotFoundError:
        print("❌ 错误: 找不到Excel文件")
        return None
    except Exception as e:
        print(f"❌ 读取数据时出错: {e}")
        return None

def analyze_question1(df):
    """分析问题1: 支持多模态处理的智能体类型占比前三"""
    # 按智能体类型分组，计算多模态占比
    agent_multimodal = df.groupby('agent_type')['multimodal_capability'].agg(['count', 'sum', 'mean']).round(4)
    agent_multimodal.columns = ['总数', '支持多模态数量', '多模态占比']

    # 按占比排序，取前三
    top3_agents = agent_multimodal.sort_values('多模态占比', ascending=False).head(3)

    print("问题1结果 - 支持多模态处理的智能体类型占比前三:")
    for idx, (agent_type, row) in enumerate(top3_agents.iterrows(), 1):
        print(f"  {idx}. {agent_type}: {row['多模态占比']:.1%} ({row['支持多模态数量']:.0f}/{row['总数']:.0f})")

    return top3_agents

def analyze_question2(df):
    """分析问题2: 支持多模态处理的大模型架构占比前三"""
    # 按大模型架构分组，计算多模态占比
    model_multimodal = df.groupby('model_architecture')['multimodal_capability'].agg(['count', 'sum', 'mean']).round(4)
    model_multimodal.columns = ['总数', '支持多模态数量', '多模态占比']

    # 按占比排序，取前三
    top3_models = model_multimodal.sort_values('多模态占比', ascending=False).head(3)

    print("问题2结果 - 支持多模态处理的大模型架构占比前三:")
    for idx, (model_arch, row) in enumerate(top3_models.iterrows(), 1):
        print(f"  {idx}. {model_arch}: {row['多模态占比']:.1%} ({row['支持多模态数量']:.0f}/{row['总数']:.0f})")

    return top3_models

def analyze_question3(df):
    """分析问题3: 各任务类别bias_detection中位数前三"""
    # 按任务类别分组，计算bias_detection_score的中位数
    task_bias = df.groupby('task_category')['bias_detection_score'].agg(['count', 'median']).round(4)
    task_bias.columns = ['总数', '中位数']

    # 按中位数排序，取前三
    top3_tasks = task_bias.sort_values('中位数', ascending=False).head(3)

    print("问题3结果 - 各任务类别bias_detection中位数前三:")
    for idx, (task_category, row) in enumerate(top3_tasks.iterrows(), 1):
        print(f"  {idx}. {task_category}: {row['中位数']:.4f} (样本数: {row['总数']:.0f})")

    return top3_tasks

def create_chart1(data):
    """生成问题1的水平柱状图"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))

    # 获取数据
    agent_types = data.index.tolist()
    percentages = (data['多模态占比'] * 100).tolist()

    # 创建水平柱状图
    bars = ax.barh(agent_types, percentages, color=['#2196F3', '#1976D2', '#0D47A1'])

    # 设置标题和标签
    ax.set_title('支持多模态处理的智能体类型占比前三', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('多模态占比 (%)', fontsize=12)
    ax.set_ylabel('智能体类型', fontsize=12)

    # 在柱子上添加数值标签
    for i, (bar, percentage) in enumerate(zip(bars, percentages)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{percentage:.1f}%', ha='left', va='center', fontsize=11)

    # 设置网格和样式
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim(0, max(percentages) * 1.2)

    plt.tight_layout()
    return fig

def create_chart2(data):
    """生成问题2的垂直柱状图"""
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))

    # 获取数据
    model_archs = data.index.tolist()
    percentages = (data['多模态占比'] * 100).tolist()

    # 创建垂直柱状图
    bars = ax.bar(model_archs, percentages, color=['#4CAF50', '#388E3C', '#2E7D32'])

    # 设置标题和标签
    ax.set_title('支持多模态处理的大模型架构占比前三', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('大模型架构', fontsize=12)
    ax.set_ylabel('多模态占比 (%)', fontsize=12)

    # 在柱子上添加数值标签
    for bar, percentage in zip(bars, percentages):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{percentage:.1f}%', ha='center', va='bottom', fontsize=11)

    # 设置网格和样式
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(percentages) * 1.2)

    # 旋转x轴标签以避免重叠
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    return fig

def create_chart3(data):
    """生成问题3的垂直柱状图"""
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))

    # 获取数据
    task_categories = data.index.tolist()
    medians = data['中位数'].tolist()

    # 创建垂直柱状图
    bars = ax.bar(task_categories, medians, color=['#FF9800', '#F57C00', '#E65100'])

    # 设置标题和标签
    ax.set_title('各任务类别bias_detection中位数前三', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('任务类别', fontsize=12)
    ax.set_ylabel('bias_detection中位数', fontsize=12)

    # 在柱子上添加数值标签
    for bar, median in zip(bars, medians):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{median:.4f}', ha='center', va='bottom', fontsize=11)

    # 设置网格和样式
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(medians) * 1.1)

    # 旋转x轴标签以避免重叠
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    return fig

def chart_to_base64(fig):
    """将matplotlib图表转换为base64编码"""
    # 创建字节流缓冲区
    buffer = BytesIO()

    # 将图表保存到缓冲区
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)

    # 转换为base64编码
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # 关闭缓冲区和图表
    buffer.close()
    plt.close(fig)

    return image_base64

def generate_html(chart1_b64, chart2_b64, chart3_b64, stats):
    """生成HTML内容"""
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI智能体性能数据看板</title>
    <style>
        /* 基础样式重置 */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #ffffff;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            border-radius: 10px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .stats-overview {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2196F3;
        }}

        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}

        .section {{
            margin-bottom: 40px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .section-header {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}

        .section-title {{
            font-size: 1.5em;
            color: #2196F3;
            margin-bottom: 10px;
        }}

        .section-description {{
            color: #666;
        }}

        .chart-container {{
            padding: 20px;
            text-align: center;
        }}

        .chart-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}

        footer {{
            text-align: center;
            padding: 30px 0;
            color: #666;
            border-top: 1px solid #e9ecef;
            margin-top: 40px;
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            h1 {{
                font-size: 2em;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .section-header {{
                padding: 15px;
            }}

            .chart-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI智能体性能数据看板</h1>
            <div class="subtitle">基于Agentic AI Performance Dataset 2025的数据分析</div>
        </header>

        <div class="stats-overview">
            <h2>数据概览</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{stats['total_records']}</div>
                    <div class="stat-label">总记录数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats['total_columns']}</div>
                    <div class="stat-label">数据字段数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats['multimodal_count']}</div>
                    <div class="stat-label">支持多模态的智能体</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats['multimodal_percentage']:.1f}%</div>
                    <div class="stat-label">多模态支持比例</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <div class="section-title">问题1: 支持多模态处理的智能体类型占比前三</div>
                <div class="section-description">分析各种智能体类型中支持多模态处理的占比情况</div>
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{chart1_b64}" alt="智能体类型多模态占比图" class="chart-image">
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <div class="section-title">问题2: 支持多模态处理的大模型架构占比前三</div>
                <div class="section-description">分析各种大模型架构中支持多模态处理的占比情况</div>
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{chart2_b64}" alt="大模型架构多模态占比图" class="chart-image">
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <div class="section-title">问题3: 各任务类别bias_detection中位数前三</div>
                <div class="section-description">分析各种任务类别的公正性检测得分中位数排名</div>
            </div>
            <div class="chart-container">
                <img src="data:image/png;base64,{chart3_b64}" alt="任务类别bias_detection中位数图" class="chart-image">
            </div>
        </div>

        <footer>
            <p>数据来源: Agentic AI Performance Dataset 2025</p>
            <p>实际处理数据: {stats['total_records']} 行 × {stats['total_columns']} 列</p>
            <p>生成时间: {stats['generation_time']}</p>
        </footer>
    </div>
</body>
</html>"""

    return html_content

def main():
    """主函数"""
    print("开始执行AI智能体性能数据分析...")

    # 1. 加载数据
    df = load_data()
    if df is None:
        print("❌ 数据加载失败，程序退出")
        return

    # 2. 分析三个问题
    print("\n" + "="*50)
    question1_result = analyze_question1(df)

    print("\n" + "="*50)
    question2_result = analyze_question2(df)

    print("\n" + "="*50)
    question3_result = analyze_question3(df)

    # 3. 生成图表
    print("\n" + "="*50)
    print("生成可视化图表...")

    chart1_fig = create_chart1(question1_result)
    chart1_b64 = chart_to_base64(chart1_fig)
    print("✅ 图表1生成完成")

    chart2_fig = create_chart2(question2_result)
    chart2_b64 = chart_to_base64(chart2_fig)
    print("✅ 图表2生成完成")

    chart3_fig = create_chart3(question3_result)
    chart3_b64 = chart_to_base64(chart3_fig)
    print("✅ 图表3生成完成")

    # 4. 准备统计信息
    from datetime import datetime
    stats = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'multimodal_count': df['multimodal_capability'].sum(),
        'multimodal_percentage': df['multimodal_capability'].mean() * 100,
        'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # 5. 生成HTML看板
    print("\n生成HTML数据看板...")
    html_content = generate_html(chart1_b64, chart2_b64, chart3_b64, stats)

    # 6. 保存HTML文件
    try:
        with open('data-dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✅ HTML看板已保存为 'data-dashboard.html'")
    except Exception as e:
        print(f"❌ 保存HTML文件时出错: {e}")
        return

    print("\n" + "="*50)
    print("🎉 分析完成! 请打开 'data-dashboard.html' 查看结果")
    print(f"📊 处理了 {stats['total_records']} 行数据")
    print(f"📈 生成了 3 个可视化图表")
    print(f"📱 支持手机浏览器查看")

if __name__ == "__main__":
    main()

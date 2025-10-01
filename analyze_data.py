# AI智能体性能数据分析脚本
# 学习目标：Python基础语法、pandas数据处理、JSON文件操作

import pandas as pd
import json
from datetime import datetime

print("=== AI智能体性能数据分析 ===")
print("开始时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 步骤1：读取Excel文件并修正列名
print("\n步骤1：读取Excel数据文件...")
try:
    # 读取Excel文件
    df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')
    
    # 使用第一行作为列标题
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])  # 删除第一行（现在是重复的标题行）
    
    # 重置索引
    df = df.reset_index(drop=True)
    
    print(f"数据读取成功！数据形状: {df.shape}")
    print(f"实际处理的数据记录数: {len(df)} 条")
    
    # 显示关键列的信息
    key_columns = ['agent_type', 'multimodal_capability', 'model_architecture', 'task_category', 'bias_detection_score']
    print("关键列检查:")
    for col in key_columns:
        if col in df.columns:
            print(f"✓ {col}: 存在")
        else:
            print(f"✗ {col}: 不存在")
            
except Exception as e:
    print(f"读取文件时发生错误: {e}")
    exit(1)

# 步骤2：问题1分析 - agent_type多模态占比排名前3
print("\n步骤2：分析问题1 - 各智能体类型的多模态处理占比...")

# 计算各agent_type中multimodal_capability为True的占比
agent_multimodal_stats = []

# 获取所有唯一的agent_type
unique_agent_types = df['agent_type'].unique()

for agent_type in unique_agent_types:
    # 筛选该agent_type的所有记录
    agent_data = df[df['agent_type'] == agent_type]
    
    # 计算总数和multimodal_capability为True的数量
    total_count = len(agent_data)
    multimodal_count = len(agent_data[agent_data['multimodal_capability'] == True])
    
    # 计算占比（百分比）
    multimodal_percentage = (multimodal_count / total_count) * 100 if total_count > 0 else 0
    
    agent_multimodal_stats.append({
        'agent_type': agent_type,
        'total_count': total_count,
        'multimodal_count': multimodal_count,
        'multimodal_percentage': round(multimodal_percentage, 2)
    })

# 按多模态占比降序排列，取前3名
agent_multimodal_stats.sort(key=lambda x: x['multimodal_percentage'], reverse=True)
top3_agents = agent_multimodal_stats[:3]

print("问题1结果：支持多模态处理占比排名前3的智能体类型")
for i, agent in enumerate(top3_agents, 1):
    print(f"{i}. {agent['agent_type']}: {agent['multimodal_percentage']}% ({agent['multimodal_count']}/{agent['total_count']})")

# 步骤3：问题2分析 - model_architecture多模态占比排名前3
print("\n步骤3：分析问题2 - 各大模型架构的多模态处理占比...")

# 计算各model_architecture中multimodal_capability为True的占比
model_multimodal_stats = []

# 获取所有唯一的model_architecture
unique_model_architectures = df['model_architecture'].unique()

for model_arch in unique_model_architectures:
    # 筛选该model_architecture的所有记录
    model_data = df[df['model_architecture'] == model_arch]
    
    # 计算总数和multimodal_capability为True的数量
    total_count = len(model_data)
    multimodal_count = len(model_data[model_data['multimodal_capability'] == True])
    
    # 计算占比（百分比）
    multimodal_percentage = (multimodal_count / total_count) * 100 if total_count > 0 else 0
    
    model_multimodal_stats.append({
        'model_architecture': model_arch,
        'total_count': total_count,
        'multimodal_count': multimodal_count,
        'multimodal_percentage': round(multimodal_percentage, 2)
    })

# 按多模态占比降序排列，取前3名
model_multimodal_stats.sort(key=lambda x: x['multimodal_percentage'], reverse=True)
top3_models = model_multimodal_stats[:3]

print("问题2结果：支持多模态处理占比排名前3的大模型架构")
for i, model in enumerate(top3_models, 1):
    print(f"{i}. {model['model_architecture']}: {model['multimodal_percentage']}% ({model['multimodal_count']}/{model['total_count']})")

# 步骤4：问题3分析 - task_category偏见检测中位数排名前3
print("\n步骤4：分析问题3 - 各任务类别的偏见检测分数中位数...")

# 计算各task_category的bias_detection_score中位数
task_bias_stats = []

# 获取所有唯一的task_category
unique_task_categories = df['task_category'].unique()

for task_cat in unique_task_categories:
    # 筛选该task_category的所有记录
    task_data = df[df['task_category'] == task_cat]
    
    # 将bias_detection_score转换为数值型（排除非数值）
    bias_scores = pd.to_numeric(task_data['bias_detection_score'], errors='coerce').dropna()
    
    if len(bias_scores) > 0:
        # 计算中位数
        median_score = bias_scores.median()
        
        task_bias_stats.append({
            'task_category': task_cat,
            'sample_count': len(bias_scores),
            'median_bias_score': round(median_score, 2)
        })

# 按偏见检测分数中位数降序排列，取前3名
task_bias_stats.sort(key=lambda x: x['median_bias_score'], reverse=True)
top3_tasks = task_bias_stats[:3]

print("问题3结果：偏见检测分数中位数排名前3的任务类别")
for i, task in enumerate(top3_tasks, 1):
    print(f"{i}. {task['task_category']}: {task['median_bias_score']} (样本数: {task['sample_count']})")

# 步骤5：保存结果为JSON文件
print("\n步骤5：保存分析结果为JSON文件...")

# 准备要保存的数据
results_data = {
    'dataset_info': {
        'total_records': len(df),
        'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'file_name': 'first-80-rows-agentic_ai_performance_dataset_20250622.xlsx'
    },
    'question1': {
        'title': '支持多模态处理占比排名前3的智能体类型',
        'description': '各智能体类型中multimodal_capability为True的占比',
        'top3_results': [
            {
                'rank': i + 1,
                'agent_type': agent['agent_type'],
                'percentage': agent['multimodal_percentage'],
                'multimodal_count': agent['multimodal_count'],
                'total_count': agent['total_count']
            }
            for i, agent in enumerate(top3_agents)
        ]
    },
    'question2': {
        'title': '支持多模态处理占比排名前3的大模型架构',
        'description': '各大模型架构中multimodal_capability为True的占比',
        'top3_results': [
            {
                'rank': i + 1,
                'model_architecture': model['model_architecture'],
                'percentage': model['multimodal_percentage'],
                'multimodal_count': model['multimodal_count'],
                'total_count': model['total_count']
            }
            for i, model in enumerate(top3_models)
        ]
    },
    'question3': {
        'title': '偏见检测分数中位数排名前3的任务类别',
        'description': '各任务类别的bias_detection_score中位数',
        'top3_results': [
            {
                'rank': i + 1,
                'task_category': task['task_category'],
                'median_score': task['median_bias_score'],
                'sample_count': task['sample_count']
            }
            for i, task in enumerate(top3_tasks)
        ]
    }
}

# 保存为JSON文件
try:
    with open('data_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    print("✓ 分析结果已保存到 data_results.json")
except Exception as e:
    print(f"✗ 保存JSON文件时发生错误: {e}")

print(f"\n=== 数据分析完成 ===")
print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
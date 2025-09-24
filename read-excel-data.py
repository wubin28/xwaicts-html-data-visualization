import pandas as pd
import json
from collections import Counter

def analyze_agentic_ai_data():
    # 读取Excel文件
    df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx')

    # 获取实际处理的记录数
    total_records = len(df)
    print(f"实际处理的数据集记录数: {total_records}")

    # 问题1: 支持多模态处理的智能体类型占比前三
    multimodal_agents = df[df['multimodal_capability'] == True]
    agent_type_counts = multimodal_agents['agent_type'].value_counts()
    agent_type_percentages = (agent_type_counts / len(multimodal_agents) * 100).round(2)
    top3_agent_types = agent_type_percentages.head(3)

    print("\n问题1 - 支持多模态处理的智能体类型占比前三:")
    for agent_type, percentage in top3_agent_types.items():
        print(f"{agent_type}: {percentage}%")

    # 问题2: 支持多模态处理的大模型架构占比前三
    model_arch_counts = multimodal_agents['model_architecture'].value_counts()
    model_arch_percentages = (model_arch_counts / len(multimodal_agents) * 100).round(2)
    top3_model_archs = model_arch_percentages.head(3)

    print("\n问题2 - 支持多模态处理的大模型架构占比前三:")
    for arch, percentage in top3_model_archs.items():
        print(f"{arch}: {percentage}%")

    # 问题3: 各任务类别的公正性中位数前三
    bias_by_task = df.groupby('task_category')['bias_detection'].median().sort_values(ascending=False)
    top3_bias_tasks = bias_by_task.head(3)

    print("\n问题3 - 各任务类别公正性中位数前三:")
    for task, median_bias in top3_bias_tasks.items():
        print(f"{task}: {median_bias}")

    # 准备JSON数据用于HTML看板
    dashboard_data = {
        "total_records": total_records,
        "multimodal_records": len(multimodal_agents),
        "agent_types": {
            "labels": list(top3_agent_types.index),
            "data": list(top3_agent_types.values),
            "title": "多模态智能体类型占比前三"
        },
        "model_architectures": {
            "labels": list(top3_model_archs.index),
            "data": list(top3_model_archs.values),
            "title": "多模态大模型架构占比前三"
        },
        "task_bias": {
            "labels": list(top3_bias_tasks.index),
            "data": list(top3_bias_tasks.values),
            "title": "任务公正性中位数前三"
        }
    }

    # 保存为JSON文件
    with open('dashboard_data.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

    print(f"\n分析结果已保存到 dashboard_data.json")
    return dashboard_data

if __name__ == "__main__":
    analyze_agentic_ai_data()
# 数据看板项目实施计划

## 项目概述
本项目旨在读取Excel数据集，进行数据分析，并生成一个响应式的HTML数据看板，回答三个关键问题，同时满足技术和设计要求。

## 实施步骤

### 1. 创建和激活虚拟环境
```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装所需依赖包
pip install pandas openpyxl matplotlib seaborn
```

### 2. 编写数据分析脚本 (analyze_data.py)
- 实现Excel数据读取功能，处理表头问题
- 实现数据清洗和预处理逻辑
- 编写三个核心问题的分析函数
- 计算并输出分析结果
- 添加生成HTML看板的功能

### 3. 开发HTML数据看板 (data-dashboard.html)
- 创建基本HTML结构和响应式CSS
- 集成内联Chart.js库
- 实现三个核心问题的可视化图表
- 确保在手机浏览器上的良好显示效果
- 添加数据统计摘要和页脚信息

## 技术方案详情

### 数据分析方案

#### 数据读取
使用pandas库，设置`skiprows=1`参数以正确读取列名：
```python
import pandas as pd
df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', skiprows=1)
```

#### 问题1: 多模态智能体类型占比
```python
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
```

#### 问题2: 多模态模型架构占比
```python
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
```

#### 问题3: 任务类别公正性中位数
```python
def analyze_task_fairness(df):
    # 按任务类别分组，计算公正性分数的中位数
    median_fairness = df.groupby('task_category')['bias_detection_score'].median()
    # 返回排名前三的结果
    return median_fairness.sort_values(ascending=False).head(3)
```

### HTML数据看板方案

#### 整体结构
- 头部：标题和数据统计摘要
- 中部：三个可视化图表区域
- 底部：页脚信息

#### CSS样式设计
- 使用浅色调配色方案（白色背景，柔和的图表颜色）
- 采用Flexbox和Grid布局实现响应式设计
- 添加媒体查询以适应不同屏幕尺寸

#### 数据可视化
- 使用内联Chart.js实现三个水平条形图
- 确保图表在小屏幕上能完整显示
- 添加数据标签和交互效果

## 资源和依赖
- Python 3.x
- pandas库：数据处理
- openpyxl库：Excel文件读取
- HTML/CSS/JavaScript：前端展示
- Chart.js：数据可视化

## 时间计划
1. 虚拟环境设置和依赖安装：约10分钟
2. 数据分析脚本开发：约30分钟
3. HTML数据看板开发：约40分钟
4. 测试和优化：约20分钟

## 交付成果
- `analyze_data.py`：完整的数据分析脚本
- `data-dashboard.html`：响应式HTML数据看板
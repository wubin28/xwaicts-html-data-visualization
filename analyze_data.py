#!/usr/bin/env python3
"""
Analyze the Agentic AI Performance dataset and generate a static HTML dashboard.
- Reads: first-80-rows-agentic_ai_performance_dataset_20250622.xlsx
- Outputs: data-dashboard.html (self-contained), with inline SVG charts

Notes:
- UI text in Chinese; code comments in English.
- Robust column detection and value normalization included.
"""
from __future__ import annotations

import io
import sys
import json
import math
import html
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Ensure headless backend
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
HTML_FILE = "data-dashboard.html"

# -----------------------------
# Helpers: column detection
# -----------------------------

def _clean_col_name(s: str) -> str:
    s = s.strip().lower()
    # normalize common separators
    for ch in ["_", "-", "/", "\\", ":", ";", "."]:
        s = s.replace(ch, " ")
    # collapse spaces
    s = " ".join(s.split())
    return s


def detect_columns(cols: List[str]) -> Dict[str, Optional[str]]:
    """Detect actual column names for canonical fields using flexible matching.
    Returns mapping: {canonical_name -> actual_column_or_None}
    Canonicals: agent_type, model_architecture, task_category, multimodal_capability, bias_detection
    """
    cleaned = {c: _clean_col_name(c) for c in cols}

    def find_first(predicate) -> Optional[str]:
        for orig, cln in cleaned.items():
            if predicate(orig, cln):
                return orig
        return None

    def contains_tokens(cln: str, tokens: List[str]) -> bool:
        return all(tok in cln for tok in tokens)

    # agent_type
    agent_col = find_first(lambda orig, cln: cln == "agent type" or contains_tokens(cln, ["agent", "type"]))

    # model_architecture
    model_col = find_first(lambda orig, cln: cln == "model architecture" or contains_tokens(cln, ["model", "architecture"]))

    # task_category
    task_col = find_first(lambda orig, cln: cln == "task category" or contains_tokens(cln, ["task"]))

    # multimodal_capability
    mm_col = find_first(
        lambda orig, cln: cln == "multimodal capability" or (
            "multimodal" in cln and ("capability" in cln or "capab" in cln or "support" in cln))
            or contains_tokens(cln, ["is", "multimodal"]) or contains_tokens(cln, ["supports", "multimodal"])
    )

    # bias detection (numeric)
    bias_col = find_first(lambda orig, cln: cln in ("bias detection", "bias score") or ("bias" in cln and ("detect" in cln or "score" in cln)))

    return {
        "agent_type": agent_col,
        "model_architecture": model_col,
        "task_category": task_col,
        "multimodal_capability": mm_col,
        "bias_detection": bias_col,
    }


# -----------------------------
# Helpers: value parsing
# -----------------------------

def parse_multimodal(series: pd.Series) -> pd.Series:
    """Map various truthy/falsey encodings to boolean; unrecognized -> NaN.
    True set: True, 1, '1', 'true', 'yes', 'y', 't', '支持', '是'
    False set: False, 0, '0', 'false', 'no', 'n', 'f', '不支持', '否'
    """
    if series is None:
        return pd.Series([np.nan] * 0)

    true_set = {True, 1, "1", "true", "yes", "y", "t", "支持", "是"}
    false_set = {False, 0, "0", "false", "no", "n", "f", "不支持", "否"}

    def norm(x):
        if pd.isna(x):
            return np.nan
        if isinstance(x, (int, float)):
            if pd.isna(x):
                return np.nan
            if int(x) == 1:
                return True
            if int(x) == 0:
                return False
        s = str(x).strip().lower()
        if s in {str(v).lower() for v in true_set}:
            return True
        if s in {str(v).lower() for v in false_set}:
            return False
        return np.nan

    return series.map(norm)


# -----------------------------
# Metrics
# -----------------------------

def compute_top3_multimodal_by(df: pd.DataFrame, group_col: str, mm_col: str) -> pd.DataFrame:
    sub = df[[group_col, mm_col]].copy()
    sub = sub[ sub[group_col].notna() ]
    sub[mm_col] = parse_multimodal(sub[mm_col])
    sub = sub[ sub[mm_col].notna() ]
    if sub.empty:
        return pd.DataFrame(columns=["label", "proportion", "n"])  # empty

    grp = sub.groupby(group_col)
    counts = grp[mm_col].agg([("n_true", lambda s: (s == True).sum()), ("n_valid", lambda s: s.notna().sum())]).reset_index()
    counts["proportion"] = counts["n_true"] / counts["n_valid"].replace(0, np.nan)
    counts = counts.dropna(subset=["proportion"])  # defensive

    # rank desc by proportion; tie-break by group name ascending
    counts = counts.sort_values(by=["proportion", group_col], ascending=[False, True])
    top3 = counts.head(3).copy()
    top3.rename(columns={group_col: "label"}, inplace=True)
    top3["n"] = top3["n_valid"]
    return top3[["label", "proportion", "n"]]


def compute_top3_bias_median(df: pd.DataFrame, group_col: str, bias_col: str) -> pd.DataFrame:
    sub = df[[group_col, bias_col]].copy()
    sub = sub[ sub[group_col].notna() ]
    sub[bias_col] = pd.to_numeric(sub[bias_col], errors="coerce")
    sub = sub[ sub[bias_col].notna() ]
    if sub.empty:
        return pd.DataFrame(columns=["label", "median", "n"])  # empty

    grp = sub.groupby(group_col)
    stats = grp[bias_col].agg([("median", "median"), ("n", "count")]).reset_index()
    stats = stats.sort_values(by=["median", group_col], ascending=[False, True])
    stats.rename(columns={group_col: "label"}, inplace=True)
    return stats.head(3)[["label", "median", "n"]]


# -----------------------------
# Visualization (SVG via Matplotlib)
# -----------------------------

def make_hbar_svg(labels: List[str], values: List[float], annotations: List[str], title: str, xlabel: str, is_percentage: bool = False) -> str:
    if len(labels) == 0:
        return ""
    sns.set_theme(style="whitegrid")
    height = max(2.5, 1.0 + 0.6 * len(labels))
    fig, ax = plt.subplots(figsize=(6.5, height))

    # Bars
    y_pos = np.arange(len(labels))
    color = sns.color_palette("pastel")[0]
    ax.barh(y_pos, values, color=color, edgecolor="#888")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)

    # X axis formatting
    if is_percentage:
        ax.set_xlim(0, max(1.0, (max(values) if values else 1.0) * 1.05))
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1.0))
    else:
        vmax = max(values) if values else 1.0
        ax.set_xlim(0, vmax * 1.10)

    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_title(title, fontsize=12, weight="bold")

    # Value labels at end of bars
    for i, v in enumerate(values):
        if is_percentage:
            txt = f"{v*100:.1f}%"
        else:
            txt = f"{v:.2f}"
        ann = annotations[i] if i < len(annotations) else ""
        ax.text(v + (0.01 if is_percentage else vmax*0.01), i, f"{txt} {ann}", va="center", fontsize=9)

    plt.tight_layout()
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight")
    plt.close(fig)
    svg = buf.getvalue()
    buf.close()
    return svg


# -----------------------------
# HTML Composer
# -----------------------------

def build_html(stats: Dict[str, int], svg_q1: Optional[str], svg_q2: Optional[str], svg_q3: Optional[str], notes: Dict[str, str]) -> str:
    def section(title: str, sub: str, svg: Optional[str]) -> str:
        if svg:
            content = svg
        else:
            content = f"<div class=\"placeholder\">数据不足</div>"
        return f"""
        <section class=\"card\">
          <h2>{html.escape(title)}</h2>
          <p class=\"sub\">{html.escape(sub)}</p>
          <div class=\"chart\">{content}</div>
        </section>
        """

    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    src = notes.get("source", DATA_FILE)

    css = """
    body { font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 0; background: #f7f7f9; color: #222; }
    .container { max-width: 980px; margin: 0 auto; padding: 16px; }
    header.card { padding: 16px 20px; background: #fff; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 16px; }
    .flex { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    @media (max-width: 720px) { .flex { grid-template-columns: 1fr; } }
    .card { padding: 16px 20px; background: #fff; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 16px; }
    .kpi { text-align: center; }
    .kpi h3 { margin: 6px 0 0; font-size: 22px; }
    .kpi p { margin: 0; color: #666; font-size: 13px; }
    h1 { margin: 0 0 4px; font-size: 24px; }
    h2 { margin: 0 0 6px; font-size: 18px; }
    .sub { margin: 0 0 8px; color: #666; font-size: 13px; }
    .chart svg { width: 100%; height: auto; }
    .placeholder { height: 120px; display: flex; align-items: center; justify-content: center; color: #999; background: #fafafa; border: 1px dashed #ddd; border-radius: 8px; }
    footer { color: #666; font-size: 12px; margin: 16px 0; }
    """

    html_str = f"""
<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
<meta charset=\"utf-8\"/>
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>
<title>数据看板 - Agentic AI Performance</title>
<style>{css}</style>
</head>
<body>
  <div class=\"container\">
    <header class=\"card\">
      <h1>Agentic AI 数据看板</h1>
      <div class=\"sub\">来源文件：{html.escape(src)} · 生成时间：{html.escape(gen_time)}</div>
      <div class=\"sub\">说明：本页为静态 HTML，图表以内嵌 SVG 呈现，移动端友好。</div>
    </header>

    <div class=\"flex\">
      <section class=\"card kpi\">
        <p>读取行数</p>
        <h3>{stats.get('read_rows', 0)}</h3>
      </section>
      <section class=\"card kpi\">
        <p>有效处理行数</p>
        <h3>{stats.get('processed_rows', 0)}</h3>
      </section>
    </div>

    {section('智能体类型的多模态支持占比 Top 3', '组内占比 = 支持多模态 / 该类型总数；柱上标注样本量 n', svg_q1)}
    {section('大模型架构的多模态支持占比 Top 3', '组内占比 = 支持多模态 / 该架构总数；柱上标注样本量 n', svg_q2)}
    {section('任务类别的“bias detection”中位数 Top 3', '按 task_category 分组，计算 bias detection 的中位数', svg_q3)}

    <footer>
      <div>方法：
        多模态占比的分子为组内 multimodal=True 数，分母为该组中 multimodal 可解析为布尔的行数；
        缺失值已剔除。并列按组名升序打破。若数据不足则显示占位卡片。
      </div>
      <div>© {datetime.now().year} Data Dashboard</div>
    </footer>
  </div>
</body>
</html>
"""
    return html_str


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    print("[INFO] Reading Excel...", file=sys.stderr)
    try:
        df = pd.read_excel(DATA_FILE, engine="openpyxl")
    except Exception as e:
        print(f"[ERROR] Failed to read {DATA_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    read_rows = int(len(df))
    print(f"[INFO] Read rows: {read_rows}")
    cols = list(df.columns)
    print(f"[INFO] Columns: {cols}")

    mapping = detect_columns(cols)
    print(f"[INFO] Detected mapping: {json.dumps(mapping, ensure_ascii=False)}")

    # Prepare masks for processed_rows union
    masks = []

    # Q1: agent_type + multimodal
    svg_q1 = None
    if mapping.get("agent_type") and mapping.get("multimodal_capability"):
        m1 = df[mapping["agent_type"]].notna()
        mm_parsed = parse_multimodal(df[mapping["multimodal_capability"]])
        m2 = mm_parsed.notna()
        mask_q1 = (m1 & m2)
        masks.append(mask_q1)
        q1 = compute_top3_multimodal_by(df.rename(columns={mapping["agent_type"]: "__grp__", mapping["multimodal_capability"]: "__mm__"}), "__grp__", "__mm__")
        if not q1.empty:
            labels = q1["label"].astype(str).tolist()
            values = q1["proportion"].astype(float).tolist()
            annotations = [f"(n={int(n)})" for n in q1["n"].tolist()]
            svg_q1 = make_hbar_svg(labels, values, annotations, "Q1 · 智能体类型 Top 3", "占比", is_percentage=True)
        else:
            svg_q1 = None
    else:
        print("[WARN] Missing columns for Q1; will render placeholder.")

    # Q2: model_architecture + multimodal
    svg_q2 = None
    if mapping.get("model_architecture") and mapping.get("multimodal_capability"):
        m1 = df[mapping["model_architecture"]].notna()
        mm_parsed = parse_multimodal(df[mapping["multimodal_capability"]])
        m2 = mm_parsed.notna()
        mask_q2 = (m1 & m2)
        masks.append(mask_q2)
        q2 = compute_top3_multimodal_by(df.rename(columns={mapping["model_architecture"]: "__grp__", mapping["multimodal_capability"]: "__mm__"}), "__grp__", "__mm__")
        if not q2.empty:
            labels = q2["label"].astype(str).tolist()
            values = q2["proportion"].astype(float).tolist()
            annotations = [f"(n={int(n)})" for n in q2["n"].tolist()]
            svg_q2 = make_hbar_svg(labels, values, annotations, "Q2 · 大模型架构 Top 3", "占比", is_percentage=True)
        else:
            svg_q2 = None
    else:
        print("[WARN] Missing columns for Q2; will render placeholder.")

    # Q3: task_category + bias detection (numeric)
    svg_q3 = None
    if mapping.get("task_category") and mapping.get("bias_detection"):
        m1 = df[mapping["task_category"]].notna()
        bias_numeric = pd.to_numeric(df[mapping["bias_detection"]], errors="coerce")
        m2 = bias_numeric.notna()
        mask_q3 = (m1 & m2)
        masks.append(mask_q3)
        q3 = compute_top3_bias_median(df.rename(columns={mapping["task_category"]: "__grp__", mapping["bias_detection"]: "__bias__"}), "__grp__", "__bias__")
        if not q3.empty:
            labels = q3["label"].astype(str).tolist()
            values = q3["median"].astype(float).tolist()
            annotations = [f"(n={int(n)})" for n in q3["n"].tolist()]
            svg_q3 = make_hbar_svg(labels, values, annotations, "Q3 · 任务类别 Top 3", "中位数", is_percentage=False)
        else:
            svg_q3 = None
    else:
        print("[WARN] Missing columns for Q3; will render placeholder.")

    processed_rows = int(pd.Series(False, index=df.index).pipe(lambda s: s | masks[0] if masks else s).pipe(lambda s: s | masks[1] if len(masks) > 1 else s).pipe(lambda s: s | masks[2] if len(masks) > 2 else s).sum())

    html_out = build_html(
        stats={"read_rows": read_rows, "processed_rows": processed_rows},
        svg_q1=svg_q1,
        svg_q2=svg_q2,
        svg_q3=svg_q3,
        notes={"source": DATA_FILE}
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"[INFO] Wrote {HTML_FILE}")

    # Print summary for quick verification
    print("[SUMMARY] Dashboard generated.")


if __name__ == "__main__":
    main()


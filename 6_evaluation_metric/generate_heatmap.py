import pandas as pd
import plotly.graph_objects as go

# === Load Excel file ===
file_path = r"ocr_evaluation\ocr_evaluation_qwen25vl_lora_original.xlsx"  # Adjust as needed
df = pd.read_excel(file_path)

# === Prepare data ===
pivot_data = df[["Filename", "WER", "CER", "SSA"]].set_index("Filename")

# === Create heatmap ===
fig = go.Figure(data=go.Heatmap(
    z=pivot_data.values,
    x=pivot_data.columns,
    y=pivot_data.index,
    colorscale="RdYlGn_r",  # red = poor, green = good
    colorbar=dict(title="Score"),
    hovertemplate="Metric: %{x}<br>File: %{y}<br>Score: %{z:.4f}<extra></extra>"
))

# === Add a readable metric guide in the subtitle or x-axis label ===
metric_legend = (
    "WER: 0.0=Perfect, <0.1=Excellent, 0.2–0.4=Moderate, >0.5=Poor | "
    "CER: <0.05=Very High, 0.05–0.1=Good, 0.1–0.3=Degraded, >0.3=Poor | "
    "SSA: >0.95=Perfect, 0.8–0.95=Acceptable, <0.8=Issues"
)

# === Update layout ===
fig.update_layout(
    title={
        "text": "📊 OCR Metric Heatmap: WER, CER, SSA",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title=f"Metric<br><span style='font-size:11px'>{metric_legend}</span>",
    yaxis_title="Document Filename",
    width=1200,
    height=700,
    font=dict(family="Arial", size=12),
)

# === Save to HTML ===
output_file = r"ocr_evaluation\ocr_evaluation_qwen25vl_lora_original_heatmap.html"
fig.write_html(output_file)

print(f"✅ Interactive heatmap saved to: {output_file}")

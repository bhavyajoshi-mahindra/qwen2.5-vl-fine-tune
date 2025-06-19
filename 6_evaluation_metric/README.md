# Image OCR Benchmark 

> **Goal**  Benchmark Qwen‑2.5 VL (base & LoRA‑fine‑tuned) against open‑source PyTesseract on a Gujarati test set, evaluating Word‑, Character‑ and Layout‑level accuracy.

> 📄 **Detailed Report**: Please refer to [`ChatGPT_Generated_Evaluation_Report.md`](ChatGPT_Generated_Evaluation_Report.md) for an in-depth comparison of all results, metrics, and insights.

> The **'reference'** folder consist of the Ground Truth of the test data which will be used to evaluate the OCR outputs. 

---

## 1 · Key Scripts

| Filename                      | Purpose                                                                                                                                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`qwen2_5_vl_inference.py`** | Runs the Qwen‑2.5 VL visual‑language model and saves a `.txt` file per input image.                                                                                                               |
| **`combine_evaluation.py`**   | Calculates **WER**, **CER** and **Custom Structural Accuracy (SSA)** by comparing each OCR file with the ground‑truth reference. Produces a consolidated Excel workbook in **`ocr_evaluation/`**. |
| **`generate_heatmap.py`**     | Reads any of the metric spreadsheets and creates an interactive Plotly heatmap (`.html`) for quick visual inspection.                                                                             |

---

## 2 · Result Sets

| System / Variant                | Folder                                            | Image Source        |
| ------------------------------- | ------------------------------------------------- | ------------------- |
| Qwen 2.5‑VL **Base** (original) | `qwen25_vl_base_original_images_results`          | raw images          |
| Qwen 2.5‑VL **Base** (enhanced) | `qwen25_vl_base_enhanced_images_results`          | restored / denoised |
| Qwen 2.5‑VL **LoRA** (original) | `qwen25_vl_lora_finetune_original_images_results` | raw images          |
| Qwen 2.5‑VL **LoRA** (enhanced) | `qwen25_vl_lora_finetune_enhanced_images_results` | restored / denoised |
| **PyTesseract** (OSS)           | `pytesseract_ocr_results`                         | baseline OCR        |

All five folders mirror the ground‑truth naming scheme (e.g. `Swarupsannidhan_0081.txt`).

---

## 3 · Metric Computation

* **WER** – Word Error Rate (0 = perfect, > 0.5 = poor)
* **CER** – Character Error Rate (< 0.05 = very high quality, > 0.3 = poor)
* **SSA** – Structural Sequence Accuracy (> 0.95 = near perfect, < 0.80 = major layout issues)

`combine_evaluation.py` traverses each result folder, aligns hypothesis to reference and appends full‑precision scores to **`ocr_evaluation/ocr_comparison_<folder>.xlsx`**.

---

## 4 · Outputs

1. **Metric spreadsheets**   `ocr_evaluation/ocr_evaluation_<model>.xlsx`
2. **Interactive heatmaps**  `heatmaps/ocr_evaluation_<model>_heatmap.html`

> Tip  Open the HTML files in any browser; hover a cell to inspect per‑page metric values.

---

## 5 · How to Reproduce

```bash
# 1. Inference on each model variant
python qwen2_5_vl_inference.py 

# 2. Get combined evaluation of result type vs ground truth
python combine_evaluation.py 

# 3. Heatmap visualisation
python generate_heatmap.py 
```

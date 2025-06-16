# Gujarati OCR Benchmark — Metric‑wise Comparison Report
**This report is ChatGPT (O3) generated**

This document summarises the performance of five OCR result sets and zooms in on **Qwen 2.5 VL (Base)** and **Qwen 2.5 VL (LoRA Fine‑Tuned)** versus **PyTesseract** across three metrics:

* **WER** – Word Error Rate (↓)
* **CER** – Character Error Rate (↓)
* **SSA** – Structural Sequence Accuracy (↑)

---

## 1 · Result Sets

| Code label    | Description                             | Pre‑processing   |
| ------------- | --------------------------------------- | ---------------- |
| **Base‑Orig** | Qwen Base on original images            | —                |
| **Base‑Enh**  | Qwen Base on enhanced/restored images   | DocRes Binarization  |
| **LoRA‑Orig** | Qwen LoRA fine‑tuned on original images | —                |
| **LoRA‑Enh**  | Qwen LoRA fine‑tuned on enhanced images | DocRes Binarization |
| **Tess**      | PyTesseract                             | —                |

---

## 2 · Aggregate Metric Averages

| Result set | Avg WER ↓ | Avg CER ↓ | Avg SSA ↑ |
| ---------- | --------- | --------- | --------- |
| Base‑Orig  | **0.636** | **0.390** | **0.249** |
| Base‑Enh   | **0.611** | **0.343** | **0.199** |
| LoRA‑Orig  | **0.537** | **0.346** | **0.315** |
| LoRA‑Enh   | **0.527** | **0.355** | **0.330** |
| **Tess**   | **0.194** | **0.087** | **0.805** |

> Ranges — WER: <0.1 Excellent · 0.2‑0.4 Moderate · >0.5 Poor   |   CER: <0.05 Very High · 0.05‑0.1 Good · >0.3 Poor   |   SSA: >0.95 Near‑Perfect · 0.8‑0.95 Acceptable · <0.8 Issues

---

## 3 · Direct Comparisons

### 3.1 Qwen Base (Orig/Enh) vs PyTesseract

| Metric  | Qwen Base (best) | PyTesseract | Gap (Base – Tess) |
| ------- | ---------------- | ----------- | ----------------- |
| **WER** | 0.611 (Enh)      | **0.194**   | **+0.417** (⚠)    |
| **CER** | 0.343 (Enh)      | **0.087**   | **+0.256** (⚠)    |
| **SSA** | 0.249 (Orig)     | **0.805**   | **−0.556** (⚠)    |

*PyTesseract vastly outperforms the base model in every dimension.*

---

### 3.2 Qwen LoRA (Fine‑Tuned) vs PyTesseract

| Metric  | Qwen LoRA (best) | PyTesseract | Gap (LoRA – Tess) |
| ------- | ---------------- | ----------- | ----------------- |
| **WER** | 0.527 (Enh)      | **0.194**   | **+0.333** (⚠)    |
| **CER** | 0.346 (Orig)     | **0.087**   | **+0.259** (⚠)    |
| **SSA** | 0.330 (Enh)      | **0.805**   | **−0.475** (⚠)    |

*Fine‑tuning narrows WER but PyTesseract maintains a decisive lead.*

---

### 3.3 Qwen Base (best) vs Qwen LoRA (best)

| Metric  | Qwen Base (best) | Qwen LoRA (best) | Improvement (LoRA – Base)   |
| ------- | ---------------- | ---------------- | --------------------------- |
| **WER** | 0.611 (Enh)      | **0.527 (Enh)**  | **−0.084 (↑14 % better)**   |
| **CER** | **0.343 (Enh)**  | 0.346 (Orig)     | +0.003 (≈ +1 %, negligible) |
| **SSA** | 0.249 (Orig)     | **0.330 (Enh)**  | **+0.081 (↑33 % better)**   |

*LoRA fine‑tuning improves word‑level accuracy and layout alignment relative to the base model, but character‑level error remains essentially unchanged.*

### 4 · Metric Winners

| Metric  | Best system         | Runner‑up             |
| ------- | ------------------- | --------------------- |
| **WER** | PyTesseract (0.194) | Qwen LoRA‑Enh (0.527) |
| **CER** | PyTesseract (0.087) | Qwen Base‑Enh (0.343) |
| **SSA** | PyTesseract (0.805) | Qwen LoRA‑Enh (0.330) |

*PyTesseract is the clear winner for every metric. The fine‑tuned model edges out the base model on WER/SSA but not enough to claim any top spot.*

---

## 5 · Recommendations

1. **Adopt PyTesseract as production baseline** until Qwen metrics drop below 0.3 WER and 0.15 CER.
2. **Augment Qwen training data** with high‑quality, layout‑preserved Gujarati pairs.
3. **Experiment with hybrid OCR**: use Qwen for niche elements (tables/figures) while PyTesseract handles bulk text.
4. **Focus on layout‑aware post‑processing** (e.g., language‑model re‑ordering) to raise SSA.

---

## 6 · Artifacts Reference

* Combined metric Excel files → `ocr_evaluation/*.xlsx`
* Interactive heatmaps → `heatmaps/*.html`
* Inference outputs → see folder names in section 1.

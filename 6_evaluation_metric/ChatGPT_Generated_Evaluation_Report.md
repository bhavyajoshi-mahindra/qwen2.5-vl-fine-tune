# Gujarati OCR Benchmark — Metric‑wise Comparison Report

**This report is ChatGPT (O3) generated**

This document summarises the performance of six OCR result sets and zooms in on **Qwen 2.5 VL (Base)** and **Qwen 2.5 VL (LoRA Fine‑Tuned)** versus **PyTesseract** across three metrics:

* **WER** – Word Error Rate (↓)
* **CER** – Character Error Rate (↓)
* **SSA** – Structural Sequence Accuracy (↑)

---

## 1 · Result Sets

| Code label    | Description                             | Pre‑processing      |
| ------------- | --------------------------------------- | ------------------- |
| **Base‑Orig** | Qwen Base on original images            | —                   |
| **Base‑Enh**  | Qwen Base on enhanced/restored images   | DocRes Binarization |
| **LoRA‑Orig** | Qwen LoRA fine‑tuned on original images | —                   |
| **LoRA‑Enh**  | Qwen LoRA fine‑tuned on enhanced images | DocRes Binarization |
| **Tess‑Orig** | PyTesseract on original images          | —                   |
| **Tess‑Enh**  | PyTesseract on enhanced images          | DocRes Binarization |

---

## 2 · Aggregate Metric Averages

| Result set | Avg WER ↓ | Avg CER ↓ | Avg SSA ↑ |
| ---------- | --------- | --------- | --------- |
| Base‑Orig  | **0.636** | **0.390** | **0.249** |
| Base‑Enh   | **0.611** | **0.343** | **0.199** |
| LoRA‑Orig  | **0.441** | **0.264** | **0.399** |
| LoRA‑Enh   | **0.527** | **0.355** | **0.330** |
| Tess‑Orig  | **0.194** | **0.087** | **0.805** |
| Tess‑Enh   | **0.174** | **0.064** | **0.815** |

> Ranges — WER: <0.1 Excellent · 0.2‑0.4 Moderate · >0.5 Poor   |   CER: <0.05 Very High · 0.05‑0.1 Good · >0.3 Poor   |   SSA: >0.95 Near‑Perfect · 0.8‑0.95 Acceptable · <0.8 Issues

---

## 3 · Direct Comparisons

### 3.1 Qwen 2.5 VL Base (Orig/Enh) vs PyTesseract

| Metric  | Qwen Base (best) | PyTesseract (best) | Gap (Base – Tess) |
| ------- | ---------------- | ------------------ | ----------------- |
| **WER** | 0.611 (Enh)      | **0.174 (Enh)**    | **+0.437** (⚠)    |
| **CER** | 0.343 (Enh)      | **0.064 (Enh)**    | **+0.279** (⚠)    |
| **SSA** | 0.249 (Orig)     | **0.815 (Enh)**    | **−0.566** (⚠)    |

*PyTesseract clearly outperforms Qwen Base across all metrics.*

---

### 3.2 Qwen 2.5 VL LoRA (Fine‑Tuned) vs PyTesseract

| Metric  | Qwen LoRA (best) | PyTesseract (best) | Gap (LoRA – Tess) |
| ------- | ---------------- | ------------------ | ----------------- |
| **WER** | 0.441 (Orig)     | **0.174 (Enh)**    | **+0.267** (⚠)    |
| **CER** | 0.264 (Orig)     | **0.064 (Enh)**    | **+0.200** (⚠)    |
| **SSA** | 0.399 (Orig)     | **0.815 (Enh)**    | **−0.416** (⚠)    |

*LoRA narrows the gap significantly compared to base, but still lags behind PyTesseract.*

---

### 3.3 Qwen 2.5 VL Base vs LoRA (Best-of-each)

| Metric  | Qwen Base (best) | Qwen LoRA (best) | Improvement (LoRA – Base)  |
| ------- | ---------------- | ---------------- | -------------------------- |
| **WER** | 0.611 (Enh)      | **0.441 (Orig)** | **−0.170 (↑27.8% better)** |
| **CER** | 0.343 (Enh)      | **0.264 (Orig)** | **−0.079 (↑23.0% better)** |
| **SSA** | 0.249 (Orig)     | **0.399 (Orig)** | **+0.150 (↑60.2% better)** |

*LoRA fine‑tuning gives substantial improvements across all metrics compared to the base model.*

---

### 3.4 PyTesseract (Original vs Enhanced)

| Metric  | PyTesseract (Orig) | PyTesseract (Enh) | Improvement (Enh – Orig)   |
| ------- | ------------------ | ----------------- | -------------------------- |
| **WER** | 0.194              | **0.174**         | **−0.020 (↑10.3% better)** |
| **CER** | 0.087              | **0.064**         | **−0.023 (↑26.4% better)** |
| **SSA** | 0.805              | **0.815**         | **+0.010 (↑1.2% better)**  |

*Even PyTesseract benefits slightly from enhancement, especially on character-level recognition.*

---

## 4 · Metric Winners

| Metric  | Best system         | Runner‑up         |
| ------- | ------------------- | ----------------- |
| **WER** | PyTesseract (0.174) | LoRA‑Orig (0.441) |
| **CER** | PyTesseract (0.064) | LoRA‑Orig (0.264) |
| **SSA** | PyTesseract (0.815) | LoRA‑Orig (0.399) |

*PyTesseract is the top performer in every metric. Fine‑tuned Qwen LoRA is a consistent runner‑up.*

---

## 5 · Recommendations

1. **Use PyTesseract as production OCR engine** until further tuning of Qwen yields competitive metrics.
2. **Improve Qwen training corpus** with curated Gujarati datasets containing structured, diverse layouts.
3. **Incorporate layout‑aware pretraining** or multimodal enhancements for better SSA.
4. **Apply post‑processing refinement** using large language models (LLMs) for output correction and alignment.
5. **Consider hybrid inference**: Combine Qwen VL for layout or visual tasks with PyTesseract for bulk text.

---

## 6 · Artifacts Reference

* Evaluation metrics → `ocr_evaluation/*.xlsx`
* Original vs Enhanced result folders → refer to filenames in Section 1
* ChatGPT-generated report → `ChatGPT_Generated_Evaluation_Report.md`

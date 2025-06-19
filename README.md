# Sarvam-AI VLM Assignment

This README consolidates all steps from ground truth generation, image enhancement, OCR extraction, model fine-tuning, and benchmarking using Qwen2.5-VL and PyTesseract OCR systems on the given images.

---

## 🔄 Overview of the Workflow

1. **Ground Truth Generation** — using Azure Mistral OCR and Google Vision OCR.
2. **Image Enhancement** — with DocRes binarization to improve OCR readability.
3. **OCR Baseline Extraction** — using PyTesseract on both original and enhanced images.
4. **Model Fine-Tuning** — training Qwen2.5-VL with ShareGPT-formatted dataset (80% train / 20% test split).
5. **Benchmarking & Evaluation** — comparing fine-tuned vs base Qwen2.5-VL vs PyTesseract.

---

## 1. 🧾 Ground Truth Generation (Azure + Google OCR)

We generate gold-standard OCR outputs by combining predictions from:

* **Azure-hosted Mistral OCR**  → `azure_mistral_gt/`
* **Google Vision API OCR**     → `gvision-gt/`

Each image yields two `.txt` outputs. Manual or rule-based consensus creates the final ground truth in:

* ✅ `ground-truth/`

> Setup involves installing dependencies from `requirements.txt` and configuring `.env` for Azure + GCP access.

---

## 2. 🖼️ Image Enhancement with DocRes

We use [DocRes](https://github.com/ZZZHANG-jx/DocRes) to preprocess historical documents via **binarization**.

### Steps:

1. Clone the repo and install dependencies via `requirements.yml`
2. Place input images in `original_images/`
3. Download pretrained weights and place them correctly.
4. Run enhancement:

```bash
python inference.py --im_path original_images --task binarization --out_folder enhanced_images
```

Output folder: `enhanced_images/`

---

## 3. 🔤 PyTesseract OCR Extraction (Baseline)

Run OCR extraction with PyTesseract on both:

* `original_images/` → `pytesseract_ocr_original_image_results/`
* `enhanced_images/` → `pytesseract_ocr_enhanced_image_results/`

### Requirements:

* Tesseract installed with Gujarati (`guj.traineddata`)
* Python packages: `pytesseract`, `pillow`

```bash
python pytesseract_ocr.py
```

> Produces `.txt` files to benchmark against ground truth.

---

## 4. 🧠 Fine-Tuning Qwen2.5-VL with LLaMA-Factory

**Prerequisite — Download Weights**
Download the Qwen 2.5‑VL base weights from the provided link and copy them to `5_finetuning_qwen25_vl/` so that LLaMA‑Factory can load the checkpoint.
Link : https://drive.google.com/drive/folders/1Wdc6IWrJbAQJx7uuG45WXYKBEvz2Tr7K?usp=sharing

### Dataset Split:

* **80% Train**
* **20% Test**

### Format:

```jsonc
{
  "messages": [
    { "role": "user", "content": "<image> Extract all the plain text..." },
    { "role": "assistant", "content": "..." }
  ],
  "images": ["/path/to/image_file.png"]
}
```

### Key Steps:

```bash
# 1. Install
pip install -e ".[torch,metrics]" --no-build-isolation

# 2. Register dataset in data/dataset_info.json
# 3. Edit config: examples/train_lora/qwen2_5vl_lora_sft.yaml

# 4. Train
llamafactory-cli train examples/train_lora/qwen2_5vl_lora_sft.yaml

# 5. Merge Adapter into Base Model
llamafactory-cli export examples/merge_lora/qwen2_5vl_lora_sft.yaml
```

---

## 5. 📊 Benchmarking & Evaluation

We benchmarked the following systems:

| Model Variant         | Source Folder                                     |
| --------------------- | ------------------------------------------------- |
| Qwen2.5-VL Base       | `qwen25_vl_base_original_images_results`          |
| Qwen2.5-VL Base (enh) | `qwen25_vl_base_enhanced_images_results`          |
| Qwen2.5-VL LoRA       | `qwen25_vl_lora_finetune_original_images_results` |
| Qwen2.5-VL LoRA (enh) | `qwen25_vl_lora_finetune_enhanced_images_results` |
| PyTesseract           | `pytesseract_ocr_results`                         |

### Metrics Computed:

* **WER**: Word Error Rate
* **CER**: Character Error Rate
* **SSA**: Structural Sequence Accuracy

### Evaluation Scripts:

```bash
python combine_evaluation.py       # Metrics Excel files
python generate_heatmap.py         # Interactive heatmap
```

> 📈 See `ocr_evaluation/` and `heatmaps/` folders for results

📄 **Detailed Comparison Report**:
Refer to [`ChatGPT_Generated_Evaluation_Report.md`](ChatGPT_Generated_Evaluation_Report.md) for metric breakdowns, charts, and insights.

---

## ✅ Final Notes

* The pipeline spans raw image preprocessing, model fine-tuning, and benchmarking.
* All results are aligned against human-curated ground truth.
* Outputs help assess layout-sensitive OCR quality for low-resource Indian languages like Gujarati.

---

🔗 Repos Used:

* [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
* [DocRes](https://github.com/ZZZHANG-jx/DocRes)
* [Tesseract](https://github.com/tesseract-ocr/tesseract)


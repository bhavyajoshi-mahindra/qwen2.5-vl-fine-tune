# Document Enhancement using DocRes

This step involves enhancing the historical scanned documents using **DocRes**: a restoration model designed to eliminate **background noise, text-bleed, stains, and other ageing artefacts** commonly found in historical images.

I use the **binarization** method from the [DocRes GitHub repository](https://github.com/ZZZHANG-jx/DocRes) to process and enhance images before OCR.

---

## 🐞 Repository Setup

### 1. Clone the Repo

```bash
git clone https://github.com/ZZZHANG-jx/DocRes.git
cd DocRes
```

### 2. Create and Activate Conda Environment from YAML

```bash
conda env create -f requirements.yml
conda activate docres_env
```

> ✅ Ensure your `requirements.yml` file is located in the root directory and captures all dependencies.

---

## 📂 Weights Download & Placement

I downloaded the **pretrained weights** from the links provided in the DocRes README and placed them as follows:

```
Put MBD model weights mbd.pkl to ./data/MBD/checkpoint/
Put DocRes model weights docres.pkl to ./checkpoints/
```

Make sure the paths match exactly or update the inference code accordingly.

---

## 🧠 Inference on Historical Document Images

To enhance and binarize my scanned images:

### 1. Prepare Input

Place your images inside the `./original_images/` directory.

### 2. Run Inference

```bash
python inference.py --im_path original_images --task binarization --out_folder enhanced_images
```

The enhanced and restored images will be saved to:

```
enhanced_images
```

The **binarization** method will improve clarity and remove noise, bleed-through, stains, and other artefacts from aged documents.

---

## 🔄 Purpose

This enhanced image set is used in the next step to:

* Improve OCR performance
* Compare OCR results before and after enhancement
* Quantify the delta using metrics such as **WER**, **CER**, and **layout alignment**

---

## ✅ Outcome

All enhanced images are saved in the enhanced_images/ directory. These enhanced images, along with the original images, are used to compare the OCR extraction quality of the Qwen 2.5 VL base model and the fine-tuned Qwen 2.5 VL model. This comparison helps evaluate the improvement in OCR accuracy post fine-tuning and image enhancement.


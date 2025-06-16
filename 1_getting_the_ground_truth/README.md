# Ground Truth Generation for Gujarati OCR Using Mistral and Google Vision

This project uses a combination of **Azure-hosted Mistral OCR** and **Google Vision OCR** models to generate high-quality ground truth text from images containing Gujarati and English content.

---

## 📁 Directory Structure

```
.
├── azure-mistral-ocr-gt.py      # Uses Azure Mistral OCR to extract text
├── gvision-ocr-gt.py            # Uses Google Cloud Vision OCR
├── requirements.txt             # Python dependency list
├── images/                      # Folder containing input images
├── azure_mistral_gt/           # Output folder for Mistral OCR results
├── gvision-gt/                 # Output folder for Google Vision OCR results
├── ground-truth/               # Final ground truth after combining both model outputs
└── .env                         # Environment file for Azure credentials
```

---

## 🛠️ Setup Instructions

### 1. Create and Activate Python Environment

```bash
conda create --name ocr_env python=3.11 -y
conda activate ocr_env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

### 1. Azure Mistral OCR – `.env` File Setup

Create a `.env` file in the root directory with the following keys:

```env
AZURE_MISTRAL_OCR_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_MISTRAL_OCR_API=<your-api-key>
AZURE_MISTRAL_OCR_DEPLOY_NAME=<your-deployment-name>
```

### 2. Google Vision OCR – JSON Key File

Ensure your Google service account key is downloaded and path-correctly referenced in `gvision-ocr-gt.py`:

```python
JSON_KEY_PATH = "google_json_key.json"
```

---

## 🚀 Running the OCR Pipelines

### A. Azure Mistral OCR

```bash
python azure-mistral-ocr-gt.py
```

* Input Folder: `images/`
* Output Folder: `azure_mistral_gt/`
* Output Format: `.txt` files with extracted markdown text from each image

### B. Google Vision OCR

```bash
python gvision-ocr-gt.py
```

* Input Folder: `E:\MVL-assigment\images`
* Output Folder: `E:\MVL-assigment\gvision-gt`
* Output Format: `.txt` files containing full OCR text from Vision API

> ⚠️ You may want to unify `IMAGE_FOLDER` and `OUTPUT_FOLDER` paths in both scripts if running across OS/platforms.

---

## ✅ Output

Each image will have two corresponding `.txt` files:

* One from Azure Mistral in `azure_mistral_gt/`
* One from Google Vision in `gvision-gt/`

### ✅ Final Ground Truth

The final ground truth was created by combining the outputs of both models manually or via consensus logic. These files are located in the `ground-truth/` folder.

These serve as the gold standard for evaluating and fine-tuning the OCR models.

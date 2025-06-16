# OCR Extraction using PyTesseract

This step involves extracting text from scanned document images using the **PyTesseract** OCR engine. I applied this to both the **original** and **DocRes-enhanced** images to compare their OCR quality.

The extracted text results will be used to evaluate and compare the performance of:

* **Base Qwen 2.5 VL OCR model**
* **Fine-tuned Qwen 2.5 VL OCR model**
* **PyTesseract OCR engine** (as an additional baseline)

---

## 🧾 Requirements

* Python 3.7+
* Tesseract OCR installed locally (with Gujarati language trained data)
* `pytesseract` and `Pillow` Python packages

### Install PyTesseract dependencies:

```bash
pip install pytesseract pillow
```

### Install Tesseract OCR Engine (Windows example):

1. Download and install from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
2. Add Tesseract to your system PATH or specify it in code:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

3. Make sure Gujarati language pack (`guj.traineddata`) is installed:

You can verify or download it from the [Tesseract tessdata repository](https://github.com/tesseract-ocr/tessdata).

---

## 📂 Directory Structure

```
.
├── pytesseract_ocr.py                                  # OCR extraction script
├── pytesseract_ocr_original_image_results/             # Output folder for Original Image OCR `.txt` files
├── pytesseract_ocr_enhanced_image_results/             # Output folder for Enhanced Image OCR `.txt` files
```

---

## 🚀 Running the Script

```bash
python pytesseract_ocr.py
```

* Input folder: `original_images/`
* Output folder: `pytesseract_ocr_original_image_results/` or `pytesseract_ocr_enhanced_image_results/`
* Language: Gujarati (`lang='guj'`)

> The script supports `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` image formats.

---

## ✅ Output

Each image will produce a `.txt` file in the `pytesseract_ocr_results/` folder containing the OCR extracted text.

These results will be used to:

* Benchmark baseline OCR performance
* Compare results from enhanced images vs original images
* Evaluate improvements achieved using the fine-tuned Qwen 2.5 VL model


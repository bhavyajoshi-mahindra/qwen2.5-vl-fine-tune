import os
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Input and output directories
input_folder = "original_images"
output_folder = "pytesseract_ocr_results"
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
valid_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

# Process each image
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    file_root, ext = os.path.splitext(filename)

    if ext.lower() not in valid_exts:
        continue

    print(f"Processing: {filename}")
    image = Image.open(file_path).convert("RGB")

    # OCR using Gujarati language
    ocr_text = pytesseract.image_to_string(image, lang='guj')

    # Save result
    with open(os.path.join(output_folder, f"{file_root}.txt"), "w", encoding="utf-8") as f:
        f.write(ocr_text)

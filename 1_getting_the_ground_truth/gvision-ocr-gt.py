import os
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image

# CONFIGURE THESE
IMAGE_FOLDER = r"E:\MVL-assigment\images"
OUTPUT_FOLDER = r"E:\MVL-assigment\gvision-gt"
JSON_KEY_PATH = "crucial-zodiac-461507-s9-a9e09952372a.json"

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Google Vision client
credentials = service_account.Credentials.from_service_account_file(JSON_KEY_PATH)
client = vision.ImageAnnotatorClient(credentials=credentials)

# Supported image extensions
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')

# Process all images in the folder
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(SUPPORTED_FORMATS):
        image_path = os.path.join(IMAGE_FOLDER, filename)

        # Load image content
        with open(image_path, "rb") as img_file:
            content = img_file.read()

        # Construct request
        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        # Extract Gujarati OCR text
        annotations = response.text_annotations
        if annotations:
            full_text = annotations[0].description
        else:
            full_text = "[No text detected]"

        # Save result in a .txt file
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(OUTPUT_FOLDER, txt_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"OCR complete for: {filename} → saved to {txt_filename}")

print("✅ OCR processing completed for all images.")

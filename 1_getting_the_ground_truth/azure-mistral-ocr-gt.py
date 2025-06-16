import os
import base64
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------------------
# Configuration
# --------------------
OCR_ENDPOINT = os.getenv("AZURE_MISTRAL_OCR_ENDPOINT")  # e.g. https://<resource>.openai.azure.com
API_KEY = os.getenv("AZURE_MISTRAL_OCR_API")           # Your Azure key
MODEL_NAME = os.getenv("AZURE_MISTRAL_OCR_DEPLOY_NAME")

INPUT_FOLDER = "images"
OUTPUT_FOLDER = "azure_mistral_gt"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def encode_image_as_data_uri(image_path):
    with open(image_path, "rb") as f:
        base64_bytes = base64.b64encode(f.read()).decode("utf-8")
        return f"data:application/png;base64,{base64_bytes}"

def create_payload(data_uri):
    return {
        "model": MODEL_NAME,
        "document": {
            "type": "image_url",
            "image_url": data_uri
        },
        "include_image_base64": True
    }

def process_image(image_path):
    data_uri = encode_image_as_data_uri(image_path)
    payload = create_payload(data_uri)

    try:
        response = requests.post(
            url=f"{OCR_ENDPOINT}/v1/ocr",
            headers=HEADERS,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed OCR for {image_path}: {e}")
        return None

def save_result(result, image_filename):
    output_filename = os.path.splitext(image_filename)[0] + ".txt"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        markdown_text = "\n\n".join(
            page.get("markdown", "").strip() for page in result.get("pages", [])
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        print(f"✅ Saved markdown to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to extract markdown for {image_filename}: {e}")


def process_folder():
    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff")):
            full_path = os.path.join(INPUT_FOLDER, file)
            print(f"Processing: {file}")
            result = process_image(full_path)
            if result:
                save_result(result, file)

if __name__ == "__main__":
    process_folder()

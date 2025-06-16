## ------ BASE MODEL INFERENCE ON ENHANCED IMAGES ------------

import os
import torch
import gc
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import time
# === Config ===
image_folder = "/content/drive/MyDrive/sarvam-ai/dataset/enhanced_image_test"
output_folder = "/content/drive/MyDrive/sarvam-ai/qwen25_vl_base_enhanced_images_results"
model_path = "/content/drive/MyDrive/sarvam-ai/qwen25_7b_instruct"
prompt_text = "Extract all the plain text from the image, both Gujarati and English keeping the structure and format consistent."

os.makedirs(output_folder, exist_ok=True)

# === Load model and processor once ===
print("🔧 Loading model and processor...")
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto",
    attn_implementation="flash_attention_2"
)
processor = AutoProcessor.from_pretrained(model_path)
tokenizer = processor.tokenizer

# === Inference loop ===
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_name in image_files:
    t1 = time.time()
    try:
        print(f"\n🖼️ Processing image: {image_name}")
        image_path = os.path.join(image_folder, image_name)

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Compose multimodal message
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt_text},
                ],
            }
        ]

        # Generate input text
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        # Prepare vision inputs
        image_inputs, video_inputs = process_vision_info(messages)

        # Prepare inputs for the model
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(model.device)

        # Inference
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                do_sample=False,
                temperature=1.0,
                max_new_tokens=2048,
                repetition_penalty=1.1,
                eos_token_id=tokenizer.eos_token_id
            )

        # Trim and decode
        generated_ids_trimmed = [
            output[len(input_ids):]
            for input_ids, output in zip(inputs.input_ids, generated_ids)
        ]
        output_text = tokenizer.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]

        # Save output
        output_file = os.path.join(output_folder, os.path.splitext(image_name)[0] + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)

        print(f"✅ Saved output to {output_file}")

    except Exception as e:
        print(f"❌ Error processing {image_name}: {e}")

    finally:
        # Free image & tensor memory after each iteration
        del image, messages, image_inputs, video_inputs, inputs
        torch.cuda.empty_cache()
        gc.collect()
    t2 = time.time()
    print(f"Time taken per image: {t2-t1}")

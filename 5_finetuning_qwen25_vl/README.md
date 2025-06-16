# Fine-Tuning **Qwen2.5-VL** with **LLaMA-Factory**

This README documents the end-to-end process I followed to fine-tune **Qwen2.5-VL** using **[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)**, merge the LoRA adapter back into the base model, and perform batch visual-language inference.

---

## 1. Prerequisites

| Tool / Library    | Version        |
| ----------------- | -------------- |
| **CUDA**          | 12.5           |
| **PyTorch**       | 2.6.0 + cu126  |
| **torchvision**   | 0.21.0 + cu126 |
| **torchaudio**    | 2.6.0 + cu126  |
| **datasets**      | 3.6.0          |
| **transformers**  | 4.52.4         |
| **accelerate**    | 1.7.0          |
| **peft**          | 0.15.2         |
| **trl**           | 0.18.2         |
| **deepspeed**     | 0.17.1         |
| **bitsandbytes**  | 0.46.0         |
| **flash-attn**    | 2.8.0.post2    |
| **triton**        | 3.2.0          |
| **LLaMA-Factory** | 0.9.3.dev0     |


## 2. Repository Setup

```bash
# Clone the repo (one-time)
git clone https://github.com/hiyouga/LLaMA-Factory.git

# Work inside the repo (mounted on Google Drive in this example)
cd LLaMA-Factory

# Editable install with Torch / metrics extras
pip install -e "[torch,metrics]" --no-build-isolation
```

---

## 3. Training Dataset Format (From `train_dataset.json`)

The dataset follows a `sharegpt` format tailored for multi-modal inputs:

```jsonc
{
  "messages": [
    { "role": "user", "content": "<image>Extract all the plain text from the image, both Gujarati and English keeping the structure and format consistent." },
    { "role": "assistant", "content": "..." }
  ],
  "images": [
    "/path/to/image_file.png"
  ]
}
```

* Each entry consists of `messages` and a list of `images`.
* `messages[0]` includes `<image>` token and a user instruction.
* `messages[1]` holds the extracted structured text.
* `images` contains image paths referenced in the messages.

---

## 4. Repository Modifications

### 4.1 Register the Dataset

`data/dataset_info.json` – add a new entry **`my_mllm_demo`**:

```jsonc
"my_mllm_demo": {
  "file_name": "path_to_train_dataset.json",
  "formatting": "sharegpt",
  "columns": { "messages": "messages", "images": "images" }
}
```
**Note : train_dataset.json is provided in 4_train_test_split**

### 4.2 Update the Training Config

`examples/train_lora/qwen2_5vl_lora_sft.yaml`

```yaml
# Replace default datasets
dataset: my_mllm_demo          # was: mllm_demo,identity,alpaca_en_demo

# Increase training epochs
num_train_epochs: 50           # was: 3.0
```

No other parameters were changed. Feel free to adjust batch size, learning rate, or LoRA rank if your hardware permits.

---

## 5. Start LoRA Fine-Tuning

```bash
llamafactory-cli train \
  LLaMA-Factory/examples/train_lora/qwen2_5vl_lora_sft.yaml
```

Key outputs:

* `output_dir` (defined in the YAML) will contain checkpoints every *n* steps.
* The best checkpoint is symlinked to `adapter_model`.

---

## 6. Merge LoRA Adapter into the Base Model

```bash
llamafactory-cli export \
  LLaMA-Factory/examples/merge_lora/qwen2_5vl_lora_sft.yaml
```

The command:

1. Loads the fine-tuned **LoRA adapter**.
2. Adds LoRA weights to **Qwen2.5-VL** base.
3. Saves a **stand-alone merged model** ready for inference.

> **Output**: `merged_model` directory (adjust path in YAML) containing
> `pytorch_model-00001-of-00002.bin`, `model.safetensors`, `config.json`, etc.

---

## 7. Batch Image-Language Inference

Run the helper script (or adapt to your own pipeline):

```bash
python qwen2_5_vl_inference.py
```

The script will:

1. Load the merged **Qwen2.5-VL** model.
2. Pair each prompt with each image (or follow your custom pairing logic).
3. Save predictions to respective folder as txt file.

---

## 8. Download the Final Model

> 📦 **Model link**:
> https://drive.google.com/drive/folders/1Wdc6IWrJbAQJx7uuG45WXYKBEvz2Tr7K?usp=sharing

---

## 9. Quantization of Fine-Tuned Qwen 2.5 VL model
1. Using AWQ
2. Using GPTA

**All the above steps are mentioned in the Qwen2_5_VL_finetune_quantize_colab.ipynb notebook**                                              
TODO: Quantized Model Inference Code 

## 10. Troubleshooting & Tips

| Symptom                 | Possible Cause                 | Quick Fix                                            |
| ----------------------- | ------------------------------ | ---------------------------------------------------- |
| **OOM during training** | Batch size too large           | Reduce `per_device_train_batch_size` or LoRA rank    |
| **Slow throughput**     | Flash-Attention not enabled    | Verify `flash_attn==2.8.0.post2` and Torch 2.6+      |
| **Tokenizer mismatch**  | Wrong `tokenizer_name_or_path` | Ensure YAML points to the same base model as weights |


import os
import numpy as np
import difflib
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# ------------------------- Metric Functions -------------------------

def wer(reference, hypothesis):
    r = reference.split()
    h = hypothesis.split()
    d = np.zeros((len(r)+1, len(h)+1), dtype=np.int32)
    for i in range(len(r)+1): d[i][0] = i
    for j in range(len(h)+1): d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
    return d[len(r)][len(h)] / float(len(r)) if len(r) > 0 else 0.0

def cer(reference, hypothesis):
    r = list(reference)
    h = list(hypothesis)
    d = np.zeros((len(r)+1, len(h)+1), dtype=np.int32)
    for i in range(len(r)+1): d[i][0] = i
    for j in range(len(h)+1): d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)
    return d[len(r)][len(h)] / float(len(r)) if len(r) > 0 else 0.0

def structural_sequence_accuracy(reference, hypothesis):
    matcher = difflib.SequenceMatcher(None, reference, hypothesis)
    matching_blocks = matcher.get_matching_blocks()
    total_chars = len(reference)
    correct = 0
    structure_penalty = 0
    for block in matching_blocks:
        for i in range(block.size):
            ref_char = reference[block.a + i]
            hyp_char = hypothesis[block.b + i]
            if ref_char == hyp_char:
                correct += 1
            elif ref_char in {' ', '\n', '\t'} or hyp_char in {' ', '\n', '\t'}:
                structure_penalty += 1
    aligned_score = max(correct - structure_penalty, 0)
    return aligned_score / total_chars if total_chars > 0 else 0.0

# ------------------------- Evaluation Function -------------------------

def evaluate_model(reference_folder, test_folder, label, output_dir):
    ref_dir = Path(reference_folder)
    test_dir = Path(test_folder)
    results = []

    for ref_file in tqdm(sorted(ref_dir.glob("*.txt")), desc=f"Evaluating {label}", unit="file"):
        test_file = test_dir / ref_file.name
        if test_file.exists():
            with open(ref_file, encoding="utf-8") as f:
                ref_text = f.read()
            with open(test_file, encoding="utf-8") as f:
                hyp_text = f.read()

            results.append({
                "Filename": ref_file.name,
                "WER": wer(ref_text, hyp_text),
                "CER": cer(ref_text, hyp_text),
                "SSA": structural_sequence_accuracy(ref_text, hyp_text)
            })

    df = pd.DataFrame(results)
    output_path = Path(output_dir) / f"ocr_comparison_{label}.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ Saved: {output_path}")
    return output_path

# ------------------------- Main Execution -------------------------

if __name__ == "__main__":
    reference_folder = "reference"
    output_dir = "ocr_comparisons"

    os.makedirs(output_dir, exist_ok=True)

    test_folders = {
        "qwen25vl_base_enhanced": "qwen25_vl_base_enhanced_images_results",
        "qwen25vl_base_original": "qwen25_vl_base_original_images_results",
        "qwen25vl_lora_enhanced": "qwen25_vl_lora_finetune_enhanced_images_results",
        "qwen25vl_lora_original": "qwen25_vl_lora_finetune_original_images_results",
        "pytesseract": "pytesseract_ocr_results"
    }

    for label, folder in test_folders.items():
        evaluate_model(reference_folder, folder, label, output_dir)

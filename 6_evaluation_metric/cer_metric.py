import numpy as np

def cer(reference, hypothesis):
    """Compute Character Error Rate (CER) using Levenshtein distance."""
    r = list(reference)
    h = list(hypothesis)
    d = np.zeros((len(r)+1, len(h)+1), dtype=np.int32)

    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j

    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(
                d[i-1][j] + 1,      # Deletion
                d[i][j-1] + 1,      # Insertion
                d[i-1][j-1] + cost  # Substitution
            )

    return d[len(r)][len(h)] / float(len(r))

# Load the files (update path as needed)
with open(r'3_opensource_ocr_inference\pytesseract_ocr_original_image_results\Swarupsannidhan_0010.txt', 'r', encoding='utf-8') as f:
    reference_text = f.read()

with open(r'3_opensource_ocr_inference\pytesseract_ocr_enhanced_image_results\Swarupsannidhan_0010_binarization.txt', 'r', encoding='utf-8') as f:
    hypothesis_text = f.read()

# Compute CER
cer_score = cer(reference_text, hypothesis_text)
print(f"Character Error Rate (CER): {cer_score:.3f}")

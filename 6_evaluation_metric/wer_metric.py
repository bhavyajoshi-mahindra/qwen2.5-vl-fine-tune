import numpy as np

def wer(reference, hypothesis):
    r = reference.split()
    h = hypothesis.split()
    d = np.zeros((len(r)+1, len(h)+1), dtype=np.int32)

    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j

    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            cost = 0 if r[i-1] == h[j-1] else 1
            d[i][j] = min(d[i-1][j] + 1,
                          d[i][j-1] + 1,
                          d[i-1][j-1] + cost)

    return d[len(r)][len(h)] / float(len(r))


# Load the files
with open(r'3_opensource_ocr_inference\pytesseract_ocr_original_image_results\Swarupsannidhan_0010.txt', 'r', encoding='utf-8') as f:
    reference_text = f.read()

with open(r'3_opensource_ocr_inference\pytesseract_ocr_enhanced_image_results\Swarupsannidhan_0010_binarization.txt', 'r', encoding='utf-8') as f:
    hypothesis_text = f.read()

# Compute WER
wer_score = wer(reference_text, hypothesis_text)
print(f"Word Error Rate (WER): {wer_score:.3f}")

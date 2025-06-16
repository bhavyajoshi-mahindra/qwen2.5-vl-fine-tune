import difflib

def structural_sequence_accuracy(reference: str, hypothesis: str) -> float:
    """
    Custom sequence-accuracy score that accounts for layout/structure alignment.
    Uses difflib to align sequences and penalizes structural mismatches.
    """
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
    accuracy = aligned_score / total_chars if total_chars > 0 else 0.0

    return accuracy

# === Load from .txt files ===
def load_text(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Replace these with your file paths
reference_path = r"3_opensource_ocr_inference\pytesseract_ocr_original_image_results\Swarupsannidhan_0011.txt"
hypothesis_path = r"3_opensource_ocr_inference\pytesseract_ocr_enhanced_image_results\Swarupsannidhan_0011_binarization.txt"

reference_text = load_text(reference_path)
hypothesis_text = load_text(hypothesis_path)

# === Compute SSA ===
ssa_score = structural_sequence_accuracy(reference_text, hypothesis_text)
print(f"Structural Sequence Accuracy (SSA): {ssa_score:.3f}")

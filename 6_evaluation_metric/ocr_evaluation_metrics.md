# OCR Evaluation Metrics Documentation

This document explains three key metrics used to evaluate the performance of OCR (Optical Character Recognition) models:

- **WER** (Word Error Rate)
- **CER** (Character Error Rate)
- **SSA** (Structural Sequence Accuracy)

---

## 📏 1. Word Error Rate (WER)

**Definition:**
Word Error Rate (WER) is a standard metric to measure the accuracy of recognized text against a reference. It calculates the minimum number of word-level edits required to transform the hypothesis into the reference.

**Formula:**

\[
WER = \frac{S + D + I}{N}
\]

Where:
- `S`: Substitutions
- `D`: Deletions
- `I`: Insertions
- `N`: Number of words in the reference

**Steps to Calculate:**
1. Split reference and hypothesis into words.
2. Use dynamic programming (Levenshtein distance) to compute edit distance.
3. Divide the total edits by the number of reference words.

**Range:**  
- 0.0 (perfect match) to >1.0 (very poor match)

**Interpretation:**
- **0.0** → Perfect word-level match.
- **<0.1** → Excellent OCR result.
- **0.2–0.4** → Moderate errors.
- **>0.5** → Low-quality output.

---

## 🔤 2. Character Error Rate (CER)

**Definition:**
Character Error Rate (CER) measures the character-level accuracy of OCR output, regardless of word boundaries.

**Formula:**

\[
CER = \frac{S + D + I}{N}
\]

Where:
- `S`, `D`, `I`: Substitutions, deletions, and insertions at the character level.
- `N`: Total number of characters in the reference.

**Steps to Calculate:**
1. Treat the text as a sequence of characters.
2. Use Levenshtein distance to calculate the edit distance.
3. Divide by total characters in the reference.

**Range:**  
- 0.0 to 1.0+

**Interpretation:**
- **<0.05** → Very high-quality OCR
- **0.05–0.1** → Good
- **0.1–0.3** → Noticeable degradation
- **>0.3** → Poor recognition

**Use Case:**  
Best suited for languages with dense character scripts (e.g., Gujarati, Chinese, Arabic).

---

## 🧱 3. Structural Sequence Accuracy (SSA)

**Definition:**
Structural Sequence Accuracy (SSA) is a custom metric that evaluates sequence similarity while accounting for **layout structure**, such as spaces, line breaks, and indentation.

**Formula:**

\[
SSA = \frac{\text{Correct Matches} - \text{Structural Penalty}}{\text{Total Reference Characters}}
\]

**Steps to Calculate:**
1. Use `difflib.SequenceMatcher` to align characters.
2. Count correct matches.
3. Penalize mismatches that involve whitespace characters (`\n`, `\t`, or space).
4. Subtract penalty and divide by total reference length.

**Range:**  
- 0.0 to 1.0

**Interpretation:**
- **>0.95** → Near-perfect structural alignment
- **0.8–0.95** → Acceptable layout fidelity
- **<0.8** → Major formatting issues

**Use Case:**  
Ideal for structured documents like PDFs, forms, tables, poetry, etc., where **format and alignment** matter as much as content.

---

## 📝 Summary Table

| Metric | Focus        | Unit      | Good Score Range | Application                        |
|--------|--------------|-----------|------------------|------------------------------------|
| WER    | Word accuracy| Word-level| < 0.1            | General OCR performance            |
| CER    | Char accuracy| Char-level| < 0.05           | Dense scripts, fine-grained errors |
| SSA    | Layout & Order| Char-level| > 0.95           | Documents with structured layouts  |

---

## ✅ Recommendation

Use **WER** for broad correctness, **CER** for detailed evaluation, and **SSA** when structure/layout matters.
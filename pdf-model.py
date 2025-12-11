import os
import re
import json
from pdf2image import convert_from_path
import easyocr

# -----------------------------
# Normalization
# -----------------------------

def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# -----------------------------
# Rolling Hash (Rabin-Karp)
# -----------------------------

def rolling_hash(text: str, pattern: str) -> bool:
    base = 257
    mod = 10**9 + 7

    n = len(text)
    m = len(pattern)

    if m > n:
        return False

    ph = 0
    th = 0
    power = 1

    for i in range(m):
        ph = (ph * base + ord(pattern[i])) % mod
        th = (th * base + ord(text[i])) % mod
        if i < m - 1:
            power = (power * base) % mod

    for i in range(n - m + 1):
        if ph == th:
            if text[i:i + m] == pattern:
                return True

        if i < n - m:
            th = (th - ord(text[i]) * power) % mod
            th = (th * base + ord(text[i + m])) % mod
            th = (th + mod) % mod

    return False

# -----------------------------
# Main logic
# -----------------------------

def extract_target_page(pdf_path: str, phrase: str, out_dir="pages", dpi=220):#adjust dpi as needed
    os.makedirs(out_dir, exist_ok=True)

    phrase_norm = normalize(phrase)
    reader = easyocr.Reader(["ru", "en"])

    pages = convert_from_path(pdf_path, dpi=dpi)

    for i, p in enumerate(pages):
        png_path = f"{out_dir}/page_{i + 1}.png"
        p.save(png_path, "PNG")

        # quick OCR
        text_chunks = reader.readtext(png_path, detail=0, paragraph=True)
        joined = normalize(" ".join(text_chunks))

        if rolling_hash(joined, phrase_norm):
            return png_path  # found target page

    return None  # not found

def extract_floats(lines):
    floats = []

    # Регулярка, которая ловит нормальные float-ы:
    #  - 1.234
    #  - .234
    #  - 1234.0
    #  - 1,234 (если вдруг OCR шалит)
    pattern = re.compile(r"\d+\.\d+|\.\d+|\d+,\d+")

    for line in lines:
        matches = pattern.findall(line)

        for m in matches:
            m = m.replace(',', '.')   # нормализация
            try:
                floats.append(float(m))
            except:
                pass

    return floats
def extract_ints(lines):
    ints = []

    pattern = re.compile(r"\b\d+\b")

    for line in lines:
        matches = pattern.findall(line)

        for m in matches:
            try:
                ints.append(int(m))
            except:
                pass

    return ints

#full ocr of detected page
def full_ocr(png_path: str):
    reader = easyocr.Reader(["ru", "en"])
    return reader.readtext(png_path, detail=1, paragraph=True)



if __name__ == "__main__":
    pdf = "pdf-parser-1/data/train/sample2.pdf"
    phrase = "city"

    target_png = extract_target_page(pdf, phrase)

    if target_png:
        print("Найдена страница:", target_png)
        data = full_ocr(target_png)
        cleaned = [item[1] for item in data]
        floats = extract_floats(cleaned)
        json_output = json.dumps(floats, ensure_ascii=False, indent=2)
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(floats, f, ensure_ascii=False, indent=2)
        print("OCR data (JSON):", json_output)
        print("OCR data:", cleaned)
    else:
        print("Страница не найдена.")

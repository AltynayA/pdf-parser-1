from pdf2image import convert_from_path
import os

def pdf_to_png(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=200)

    for i, page in enumerate(pages):
        out = os.path.join(output_folder, f"page_{i+1}.png")
        page.save(out, "PNG")
        print(f"Saved: {out}")

pdf_to_png("data/train/KEQ-FV-and-PV-tables.pdf", "data/train/KEQ-FV-and-PV-tables")

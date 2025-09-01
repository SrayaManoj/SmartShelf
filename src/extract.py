"""
extract.py
Modules for extracting file contents from different file types:
 - PDF
 - Images
 - TXT

Dependencies:
 - PyPDF2
 - pytesseract
 - pillow
"""

import os
import pypdf
import pytesseract
from PIL import Image


# --------- PDF Extraction ----------
def extract_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        # Open the PDF in binary mode
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)

            # Loop through all pages
            for page in reader.pages:
                page_text = page.extract_text()

                # Only add text if extraction worked
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] Could not extract PDF {file_path}: {e}")

    return text.strip()


# --------- Image Extraction (OCR) ----------
def extract_from_image(file_path: str) -> str:
    """Extract text from an image file using OCR."""
    text = ""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[ERROR] Could not extract Image {file_path}: {e}")
    return text.strip()


# --------- TXT Extraction ----------
def extract_from_txt(file_path: str) -> str:
    """Read plain text files directly."""
    text = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"[ERROR] Could not extract TXT {file_path}: {e}")
    return text.strip()


# --------- General Extraction Wrapper ----------
def extract_text(file_path: str) -> str:
    """Extract text depending on file type."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_from_image(file_path)
    elif ext == ".txt":
        return extract_from_txt(file_path)
    else:
        print(f"[WARN] Unsupported file type: {file_path}")
        return ""


# --------- Test Run ----------
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if os.path.exists(file):
            print(f"\nExtracting from: {file}")
            print(extract_text(file)[:300])  # print first 300 chars
        else:
            print(f"[WARN] File not found: {file}")
    else:
        print("Usage: python src/extract.py <file_path>")


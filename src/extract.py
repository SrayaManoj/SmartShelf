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
# --------- Test Run ----------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python src/extract.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    # Extract the text
    extracted_text = extract_text(file_path)

    if extracted_text:
        # Make sure processed/ folder exists
        os.makedirs("processed", exist_ok=True)

        # Build output filename (same name as input, but .txt)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        out_file = os.path.join("processed", base_name + ".txt")

        # Save to processed/ folder
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"[INFO] Extracted text saved to: {out_file}")
    else:
        print("[WARN] No text extracted.")


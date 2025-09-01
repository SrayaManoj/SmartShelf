"""
extract.py
Modules for extracting file contents from diffrent file types:
 -PDF
 -Images
 -TXT

Dependencies
 -PyPDF2
 -pytesseract
 -pillow
"""
import os
import PyPDF2
import pytesseract
from PIL import Image

#pdf extraction---
def extract_from_pdf(file_path:str)->str:
  """Extract text from a PDF file."""
text = ""
try:
     # Open the PDF in binary mode
     with open(file path:"rb") as f:
     reader=PyPDF2.PdfReader(f)
     # Loop through all pages
            for page in reader.pages:
                page_text = page.extract_text()

                # Only add text if extraction worked
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] Could not extract PDF {file_path}: {e}")

    return text.strip()
import io
import easyocr
from PIL import Image
import numpy as np
from pdf2image import convert_from_bytes
import streamlit as st
import fitz  # PyMuPDF

@st.cache_data
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)
@st.cache_data
def extract_text_from_pdf(pdf_bytes):
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    reader = easyocr.Reader(['en'], gpu=False)
    all_text = ""

    for i in range(len(pdf_document)):
        page = pdf_document[i]
        pix = page.get_pixmap(dpi=200)  # Render at good resolution
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        st.image(img, caption=f"Page {i + 1}", use_column_width=True)

        img_np = np.array(img)  # Convert PIL Image to NumPy array
        result = reader.readtext(img_np, detail=0)
        text = " ".join(result)
        all_text += f"\n\n--- Page {i + 1} ---\n{text}"

    return all_text.strip()
# @st.cache_data
# def extract_text_from_pdf(pdf_bytes):
#     images = convert_from_bytes(pdf_bytes)
#     reader = easyocr.Reader(['en'], gpu=False)

#     all_text = ""
#     for i, page_image in enumerate(images):
#         st.image(page_image, caption=f"PDF Page {i+1}", use_column_width=True)
#         result = reader.readtext(page_image, detail=0)
#         text = " ".join(result)
#         all_text += f"\n\n--- Page {i+1} ---\n{text}"

#     return all_text.strip()
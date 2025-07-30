import streamlit as st
from PIL import Image
import os

from load_mistral import load_mistral_model
from ocr_reader import extract_text_from_image
from process_with_mistral import ask_mistral

st.set_page_config(page_title="Offline Mistral OCR", layout="centered")
st.title("📄 Offline OCR with Mistral")

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save temporarily
    temp_path = "temp_image.jpg"
    image.save(temp_path)

    if st.button("🧠 Run OCR"):
        with st.spinner("Extracting text..."):
            ocr_text = extract_text_from_image(temp_path)
            st.subheader("📝 OCR Text")
            st.text_area("Raw OCR Output", ocr_text, height=200)

        if st.button("✨ Clean with Mistral"):
            with st.spinner("Loading Mistral model..."):
                tokenizer, model = load_mistral_model()

            prompt = f"Clean and correct the following OCR text:\n\n{ocr_text}"
            with st.spinner("Generating response..."):
                response = ask_mistral(model, tokenizer, prompt)
            st.subheader("🧾 Cleaned Text")
            st.text_area("Mistral Output", response, height=200)

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)
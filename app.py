# import streamlit as st
# from PIL import Image
# import os

# from load_mistral import load_mistral_model
# from ocr_reader import extract_text_from_image
# from process_with_mistral import ask_mistral

# st.set_page_config(page_title="Offline Mistral OCR", layout="centered")
# st.title("📄 Offline OCR with Mistral")

# uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# if uploaded_image is not None:
#     image = Image.open(uploaded_image)
#     st.image(image, caption="Uploaded Image", use_container_width=True)
#     # Convert if image has alpha channel
#     if image.mode == "RGBA":
#         image = image.convert("RGB")

#     # Save temporarily
#     temp_path = "temp_image.jpg"
#     image.save(temp_path)

#     if st.button("🧠 Run OCR"):
#         with st.spinner("Extracting text..."):
#             ocr_text = extract_text_from_image(temp_path)
#             st.subheader("📝 OCR Text")
#             st.text_area("Raw OCR Output", ocr_text, height=200)

#         if st.button("✨ Clean with Mistral"):
#             with st.spinner("Loading Mistral model..."):
#                 tokenizer, model = load_mistral_model()

#             prompt = f"Clean and correct the following OCR text:\n\n{ocr_text}"
#             with st.spinner("Generating response..."):
#                 response = ask_mistral(model, tokenizer, prompt)
#             st.subheader("🧾 Cleaned Text")
#             st.text_area("Mistral Output", response, height=200)

#     # Cleanup
#     if os.path.exists(temp_path):
#         os.remove(temp_path)
import streamlit as st
from PIL import Image
import os

from load_mistral import load_mistral_model
from ocr_reader import extract_text_from_image, extract_text_from_pdf
from process_with_mistral import ask_mistral, get_structured_markdown

st.set_page_config(page_title="Offline Mistral OCR", layout="centered")
st.title("📄 Offline OCR with Mistral")

uploaded_file = st.file_uploader("Upload an Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

ocr_text = ""

if uploaded_file is not None:
    file_type = uploaded_file.type

    if "image" in file_type:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Save temporarily
        temp_path = "temp_image.jpg"
        image.save(temp_path)

        if st.button("🧠 Run OCR on Image"):
            with st.spinner("Extracting text from image..."):
                # ocr_text = extract_text_from_image(temp_path)
                st.session_state.ocr_text = extract_text_from_image(temp_path)
            st.subheader("📝 OCR Text")
            st.text_area("Raw OCR Output", ocr_text, height=200)

            os.remove(temp_path)

    elif "pdf" in file_type:
        if st.button("🧠 Run OCR on PDF"):
            with st.spinner("Extracting text from PDF..."):
                pdf_bytes = uploaded_file.read()
                # ocr_text = extract_text_from_pdf(pdf_bytes)
                st.session_state.ocr_text = extract_text_from_pdf(pdf_bytes)
            ocr_text = st.session_state.ocr_text
            st.subheader("📝 OCR Text")
            st.text_area("Raw OCR Output", ocr_text, height=400)
            
            # with st.spinner("Loading Mistral model..."):
            #     tokenizer, model = load_mistral_model()

            # with st.spinner("Structuring text with Mistral..."):
            #     markdown_output = get_structured_markdown(model, tokenizer, ocr_text)

            # st.subheader("📄 Structured Markdown Output")
            # st.code(markdown_output, language="markdown")

            # st.markdown("---")
            # st.subheader("🖼️ Rendered Markdown Preview")
            # st.markdown(markdown_output, unsafe_allow_html=True)
            # st.text_area("Raw OCR Output", markdown_output, height=400)
            # # Download button
            # st.download_button(
            #     label="⬇️ Download Markdown File",
            #     data=markdown_output,
            #     file_name="structured_output.md",
            #     mime="text/markdown"
            # )
            


# if ocr_text:
#     if st.button("✨ Clean with Mistral"):
#         with st.spinner("Loading Mistral model..."):
#             tokenizer, model = load_mistral_model()

#         prompt = f"Clean and correct the following OCR text:\n\n{ocr_text}"
#         with st.spinner("Generating response..."):
#             response = ask_mistral(model, tokenizer, prompt)

#         st.subheader("🧾 Cleaned Text")
#         st.text_area("Mistral Output", response, height=400)

if "ocr_text" in st.session_state:
    ocr_text = st.session_state.ocr_text
    if st.button("🧱 Convert to Structured Markdown"):
        with st.spinner("Loading Mistral model..."):
            tokenizer, model = load_mistral_model()

        with st.spinner("Structuring text with Mistral..."):
            markdown_output = get_structured_markdown(model, tokenizer, ocr_text)

        st.subheader("📄 Structured Markdown Output")
        st.code(markdown_output, language="markdown")

        st.markdown("---")
        st.subheader("🖼️ Rendered Markdown Preview")
        st.markdown(markdown_output, unsafe_allow_html=True)
        # Download button
        st.download_button(
            label="⬇️ Download Markdown File",
            data=markdown_output,
            file_name="structured_output.md",
            mime="text/markdown"
        )
        

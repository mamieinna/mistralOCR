import sys
import os
from PIL import Image
import fitz  # PyMuPDF
import easyocr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import io

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    reader = easyocr.Reader(['en'], gpu=False)
    all_text = ""

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        result = reader.readtext(img, detail=0)
        text = " ".join(result)
        all_text += f"\n\n--- Page {i + 1} ---\n{text}"

    return all_text.strip()

def load_mistral_model():
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    return tokenizer, model

def ask_mistral(tokenizer, model, prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
    output = model.generate(input_ids, max_new_tokens=1024)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def get_structured_markdown(tokenizer, model, raw_text):
    prompt = f"""
You are a Markdown formatting assistant. Convert the following OCR-extracted text into clean, structured Markdown with headings, bullet points, and tables as needed.

Input:
{raw_text}

Output (Markdown only):
"""
    return ask_mistral(tokenizer, model, prompt)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_cli.py <file_path>")
        return

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    ext = os.path.splitext(file_path)[-1].lower()

    print("[INFO] Performing OCR...")
    if ext in ['.jpg', '.jpeg', '.png']:
        ocr_text = extract_text_from_image(file_path)
    elif ext == '.pdf':
        ocr_text = extract_text_from_pdf(file_path)
    else:
        print("Unsupported file type.")
        return

    print("\n[OCR TEXT EXTRACTED]")
    print("="*50)
    print(ocr_text[:1000] + ("..." if len(ocr_text) > 1000 else ""))  # Preview first 1000 chars
    print("="*50)

    print("[INFO] Loading Mistral model...")
    tokenizer, model = load_mistral_model()

    print("[INFO] Structuring text with Mistral...")
    markdown_output = get_structured_markdown(tokenizer, model, ocr_text)

    print("\n[STRUCTURED MARKDOWN OUTPUT]")
    print("="*50)
    print(markdown_output)
    print("="*50)

    # Optional: save to file
    output_file = os.path.splitext(file_path)[0] + "_output.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"[✅] Markdown saved to {output_file}")

if __name__ == "__main__":
    main()
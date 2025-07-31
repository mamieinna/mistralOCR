# def ask_mistral(model, tokenizer, prompt):
#     input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
#     output = model.generate(input_ids, max_new_tokens=200)
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response

def ask_mistral(model, tokenizer, prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
    output = model.generate(input_ids,max_new_tokens=1024)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

def get_structured_markdown(model, tokenizer, raw_text):
    prompt = f"""
You are a Markdown generator assistant. Convert the following OCR-extracted text into clean and structured **Markdown**.

Rules:
- Use proper **headings** (##, ###) where appropriate
- Convert lists into **bullet points**
- Use **tables** for tabular data like invoices or records
- Fix any spelling errors if obvious
- Keep important fields like dates, names, amounts clearly formatted

Text:
{raw_text}

Now output the cleaned version **only as Markdown**, no explanations.
"""
    return ask_mistral(model, tokenizer, prompt)
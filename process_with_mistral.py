def ask_mistral(model, tokenizer, prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
    output = model.generate(input_ids, max_new_tokens=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response
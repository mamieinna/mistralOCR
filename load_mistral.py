from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st

@st.cache_resource
def load_mistral_model():
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    # model = AutoModelForCausalLM.from_pretrained(model_name)
    print("tokenizer",tokenizer)
    # Save locally
    tokenizer.save_pretrained("./local_model_dir")
    model.save_pretrained("./local_model_dir")
    return tokenizer, model
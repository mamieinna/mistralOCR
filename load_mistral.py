from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

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
    return tokenizer, model
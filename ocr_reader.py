import easyocr
from PIL import Image

@st.cache_data
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)
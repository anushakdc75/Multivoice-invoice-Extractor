from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(prompt, image, input_text):
    response = model.generate_content([prompt, image[0], input_text])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multilanguage Invoice Extractor", layout="wide")

st.title("📄 Gemini Invoice Reader")
st.markdown("### Upload your invoice image and ask any question about it!")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"], label_visibility="visible")
    with col2:
        input_text = st.text_input("Ask your question:", placeholder="e.g., What is the total amount?", key="input")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_container_width=True)

submit = st.button("🔍 Analyze Invoice", use_container_width=True)

input_prompt = """You are an expert in understanding invoices.
We will upload an image as an invoice and you will answer questions based on that uploaded invoice."""

if submit:
    if uploaded_file is not None:
        with st.spinner("Analyzing the invoice..."):
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input_text)
        st.success("✅ Analysis complete!")
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please upload an invoice image first!")

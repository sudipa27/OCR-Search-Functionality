import pytesseract
from PIL import Image
import streamlit as st
import re

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from an image, supporting both English and Hindi
def extract_text_from_image(image):
    # Specify both English and Hindi language
    return pytesseract.image_to_string(image, lang='eng+hin')

# Function to highlight search keywords
def highlight_keywords(text, keywords):
    pattern = '|'.join(re.escape(keyword.strip()) for keyword in keywords.split(','))
    pattern = f'({pattern})'
    highlighted_text = re.sub(pattern, r'<mark class="highlighted">\1</mark>', text, flags=re.IGNORECASE)
    return highlighted_text

# Main Streamlit app
def main():
    st.sidebar.title("OCR and Search Options")
    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    search_keywords = st.sidebar.text_input("Enter keywords to search (comma-separated)")

    st.title("Image OCR and Keyword Search App")
    st.write("This app allows you to extract text from an image in English or Hindi, and search for specific keywords.")

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # OCR Process
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image)

        st.subheader("Extracted Text:")
        st.text_area("Extracted Text", value=extracted_text, height=200)

        if search_keywords:
            highlighted_text = highlight_keywords(extracted_text, search_keywords)
            num_results = len(re.findall(search_keywords, extracted_text, re.IGNORECASE))

            st.subheader(f"Search Results (found {num_results} match(es)):")
            st.markdown(highlighted_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

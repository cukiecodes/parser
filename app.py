import tempfile
import os
from extract_text import extract_text_from_pdf
from call2llm import get_response, get_continued_response  # Import specific functions instead of importing everything from call2llm
import streamlit as st
import json
def main():
    st.title("MCQ Parser")


    uploaded_files = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])
    pdf_files = []

    # Process uploaded PDFs
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        pdf_files.append((uploaded_file.name, temp_file_path))
    
    # Two-column layout for start and end pages
    col1, col2 = st.columns(2)

    # Convert PDFs to text
    converted_texts = []
    for i, (file_name, file_path) in enumerate(pdf_files):
        # Input fields for start and end pages
        with col1:
            start_page = st.number_input(f"Start Page ({file_name})", min_value=1, value=1, key=f"start_page_{i}")
        with col2:
            end_page = st.number_input(f"End Page ({file_name})", min_value=start_page, value=start_page, key=f"end_page_{i}")

        # Convert PDF to text
        text = extract_text_from_pdf(file_path, start_page, end_page)
        converted_texts.append(text)
        st.write(converted_texts)
    
    if st.button("Convert to JSON Format"):
        response_placeholder = st.code("")
        print("calling llm")
        combined_text = "\n".join(converted_texts)
        response = ""
        response = get_response(combined_text + "Given above are mcq questions. Return them in json format as an array of {question_num: question: option_a: option_b: option_c: option_d: answer: }, leave answer as blank if not given, dont makeup an answer", response_placeholder)
        st.table(json.loads(response))
    # Delete temporary files
    for _, file_path in pdf_files:
        os.remove(file_path)

if __name__ == "__main__":
    main()

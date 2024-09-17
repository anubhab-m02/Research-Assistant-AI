import PyPDF2
import streamlit as st

def extract_text_from_pdf(pdf_file) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        if not text.strip():
            st.warning(f"Warning: No text extracted from {pdf_file.name}. The PDF might be scanned or protected.")
        else:
            st.success(f"Successfully extracted {len(text)} characters from {pdf_file.name}")
        
        return text
    except Exception as e:
        st.error(f"Error extracting text from {pdf_file.name}: {str(e)}")
        return ""

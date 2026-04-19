import streamlit as st
import pandas as pd
import re
from .preprocess import split_into_sentences

# Try to import PDF libraries
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# Try to import docx for Word files
try:
    import docx
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False


def extract_text_from_pdf(file):
    # Extract text from PDF file
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def extract_text_from_docx(file):
    # Extract text from Word file
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""


def process_uploaded_file(uploaded_file):
    # Auto-detect file type and extract sentences
    file_name = uploaded_file.name.lower()
    content = None
    
    # CSV file
    if file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        if 'text' in df.columns:
            return df['text'].tolist()
        else:
            st.error("CSV must have a 'text' column")
            return []
    
    # TXT file
    elif file_name.endswith('.txt'):
        content = uploaded_file.read().decode('utf-8')
    
    # PDF file
    elif file_name.endswith('.pdf') and PDF_SUPPORT:
        content = extract_text_from_pdf(uploaded_file)
    
    # DOCX file
    elif file_name.endswith('.docx') and DOCX_SUPPORT:
        content = extract_text_from_docx(uploaded_file)
    
    else:
        st.error(f"Unsupported file type: {file_name}")
        return []
    
    # Split into sentences
    if content:
        return split_into_sentences(content)
    
    return []
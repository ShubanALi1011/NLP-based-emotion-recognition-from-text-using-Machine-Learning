import re
import string

def clean_text(text):
    # Simple text cleaning
    if not isinstance(text, str):
        text = str(text)
    
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join([ch for ch in text if not ch.isdigit()])
    text = ' '.join(text.split())
    
    return text

def split_into_sentences(text):
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    return sentences
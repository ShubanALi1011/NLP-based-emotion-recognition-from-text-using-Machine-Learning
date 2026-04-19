import streamlit as st
import joblib
from .config import MODELS_DIR, MODEL_FILES, VECTORIZER_FILE, ENCODER_FILE


@st.cache_resource
def load_vectorizer():
    """Load BoW vectorizer"""
    path = MODELS_DIR / VECTORIZER_FILE
    if path.exists():
        return joblib.load(path)
    return None


@st.cache_resource
def load_encoder():
    """Load label encoder"""
    path = MODELS_DIR / ENCODER_FILE
    if path.exists():
        return joblib.load(path)
    return None


@st.cache_resource
def load_all_models():
    """Load all models"""
    models = {}
    
    for name, filename in MODEL_FILES.items():
        path = MODELS_DIR / filename
        if path.exists():
            models[name] = joblib.load(path)
    
    return models
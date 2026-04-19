import sys
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Import all functions from src
from src import (
    load_vectorizer, load_encoder, load_all_models,
    process_uploaded_file, predict_emotion,
    get_emotion_color, get_emotion_emoji, plot_confidence_scores,
    PDF_SUPPORT, DOCX_SUPPORT
)

# PAGE CONFIG
st.set_page_config(
    page_title="Emotion Detection System",
    page_icon="🎭",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
    }
    .main-header p {
        color: #e0e0e0;
        margin: 0.5rem 0 0 0;
    }
    
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        animation: fadeIn 0.5s;
        width: 100%;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .emotion-title {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.8rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
    
    .example-card {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    
    .info-box {
        background: #e8f4f8;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main-header">
    <h1>🎭 Emotion Detection System</h1>
    <p>Advanced NLP-based emotion recognition from text using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# LOAD MODELS
with st.spinner("Loading models..."):
    vectorizer = load_vectorizer()
    encoder = load_encoder()
    models = load_all_models()

if not vectorizer or not models:
    st.error("Models not found! Please check the models directory.")
    st.stop()

# SIDEBAR
with st.sidebar:
    st.markdown("## 🎭 Emotion Detection")
    st.markdown("---")
    
    st.markdown("### 🤖 Model")
    selected_model = st.selectbox("", list(models.keys()))
    
    st.markdown("---")
    
    st.markdown("### 📊 Emotions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("😠 **Anger**")
        st.markdown("😨 **Fear**")
        st.markdown("😊 **Joy**")
    with col2:
        st.markdown("❤️ **Love**")
        st.markdown("😢 **Sadness**")
        st.markdown("😲 **Surprise**")
    
    st.markdown("---")
    
    st.markdown("### 📈 Performance")
    st.markdown("**Accuracy:** 89.7%")
    st.markdown("**F1-Score:** 87.3%")
    st.markdown("**Best Model:** XGBoost")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("Detects emotions from text using Machine Learning with Bag-of-Words features.")

# TABS
tab1, tab2, tab3 = st.tabs(["Single Text", "Batch Processing", "Examples"])

# TAB 1: Single Text
with tab1:
    st.markdown("### Enter Text for Analysis")
    
    user_input = st.text_area(
        "",
        placeholder="Example: I am really excited about this new project!",
        height=100,
        key="text_input"
    )
    
    if st.button("🔍 Analyze Emotion", use_container_width=True):
        if user_input and len(user_input.strip()) >= 3:
            with st.spinner("Analyzing text..."):
                model = models[selected_model]
                emotion, confidence, probabilities = predict_emotion(
                    user_input, model, vectorizer, encoder
                )
            
            if emotion:
                color = get_emotion_color(emotion)
                emoji = get_emotion_emoji(emotion)
                
                st.markdown(f"""
                <div class="result-box" style="background-color: {color}10; border: 2px solid {color};">
                    <div style="font-size: 1.2rem; color: {color}; font-weight: bold;">Detected Emotion</div>
                    <div class="emotion-title" style="color: {color};">{emoji} {emotion.upper()}</div>
                    <div style="font-size: 1.2rem; color: {color};">Confidence: {confidence:.1%}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if len(probabilities) > 1:
                    st.markdown("### Confidence Distribution")
                    fig = plot_confidence_scores(probabilities)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
            else:
                st.error("Unable to analyze. Please try different text.")
        elif user_input:
            st.warning("Please enter at least 3 characters")
        else:
            st.info("Enter some text and click 'Analyze Emotion'")

# TAB 2: Batch Processing
with tab2:
    st.markdown("### Upload File for Batch Analysis")
    
    st.markdown("""
    <div class="info-box">
        📁 Supported: CSV, TXT, PDF, DOCX (Word)
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'txt', 'pdf', 'docx'],
        help="Upload CSV (with 'text' column), TXT, PDF, or Word document"
    )
    
    if uploaded_file:
        with st.spinner("Processing file..."):
            sentences = process_uploaded_file(uploaded_file)
        
        if sentences:
            st.success(f"✅ Loaded {len(sentences)} sentences")
            
            with st.expander("Preview (first 10 sentences)"):
                for i, sent in enumerate(sentences[:10]):
                    st.write(f"{i+1}. {sent[:150]}..." if len(sent) > 150 else f"{i+1}. {sent}")
            
            if st.button("🚀 Start Analysis", use_container_width=True):
                with st.spinner(f"Analyzing {len(sentences)} sentences..."):
                    results = []
                    model = models[selected_model]
                    progress_bar = st.progress(0)
                    
                    for idx, sent in enumerate(sentences):
                        emotion, confidence, _ = predict_emotion(
                            sent, model, vectorizer, encoder
                        )
                        results.append({
                            'text': sent[:100] + "..." if len(sent) > 100 else sent,
                            'emotion': emotion,
                            'confidence': f"{confidence:.2%}"
                        })
                        progress_bar.progress((idx + 1) / len(sentences))
                    
                    results_df = pd.DataFrame(results)
                    st.success("✅ Analysis Complete!")
                    st.dataframe(results_df, use_container_width=True)
                    
                    csv_data = results_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results (CSV)",
                        csv_data,
                        f"emotion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
                    
                    st.markdown("#### Emotion Distribution")
                    chart_data = results_df['emotion'].value_counts()
                    st.bar_chart(chart_data)

# TAB 3: Examples
with tab3:
    st.markdown("### Test with Examples")
    
    examples = [
        "The movie was okay, I guess. Some parts were good, others not so much.",
        "I received the package today, but half the items were damaged.",
        "My boss said my work is improving, which is nice I suppose.",
        "The weather is cloudy today, but at least it's not raining.",
        "I'm not sure how to feel about this news. It's both good and bad.",
        "After waiting for an hour, they finally called my name.",
        "The food was decent, but the service could have been better.",
        "I think I did okay on the test, but I'm nervous about the results.",
        "My friend said she might visit next month, if she has time.",
        "The new phone has some cool features, but it's quite expensive."
    ]
    
    if 'example_results' not in st.session_state:
        st.session_state.example_results = {}
    
    for idx, example in enumerate(examples):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div class="example-card">
                <strong>{idx+1}.</strong> {example}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("Analyze", key=f"ex_{idx}", use_container_width=True):
                model = models[selected_model]
                emotion, confidence, probs = predict_emotion(
                    example, model, vectorizer, encoder
                )
                st.session_state.example_results[idx] = (emotion, confidence, probs)
                st.rerun()
        
        if idx in st.session_state.example_results:
            emotion, confidence, probs = st.session_state.example_results[idx]
            color = get_emotion_color(emotion)
            emoji = get_emotion_emoji(emotion)
            
            st.markdown(f"""
            <div style="background-color: {color}10; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {color};">
                <strong style="color: {color};">Prediction:</strong> {emoji} {emotion.upper()} 
                <span style="color: #666;">(Confidence: {confidence:.1%})</span>
            </div>
            """, unsafe_allow_html=True)
            
            if len(probs) > 1:
                fig = plot_confidence_scores(probs, title=f"Emotion Distribution - Example {idx+1}")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
        
        st.markdown("---")
    
    st.markdown("### Download Sample Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sample_df = pd.DataFrame({'text': examples})
        st.download_button(
            "📥 Download Sample CSV",
            sample_df.to_csv(index=False),
            "sample_emotions.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        sample_txt = "\n".join(examples)
        st.download_button(
            "📥 Download Sample TXT",
            sample_txt,
            "sample_emotions.txt",
            "text/plain",
            use_container_width=True
        )

# FOOTER
st.markdown("""
<div class="footer">
    <p>🎭 <strong>Emotion Detection System</strong> | Built by <strong style="color: #667eea;">Shuban Ali</strong></p>
    <p style="font-size: 0.7rem; opacity: 0.7;">© 2026 | NLP-based Emotion Recognition</p>
</div>
""", unsafe_allow_html=True)
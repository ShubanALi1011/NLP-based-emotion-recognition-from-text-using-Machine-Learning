# NLP-based Emotion Recognition from Text using Machine Learning

A comprehensive Machine Learning pipeline designed to detect six distinct emotions from text based on linguistic features. This project features a modular architecture, a high-performance prediction engine, and a user-friendly Streamlit web interface.

-----

## Project Architecture

The repository follows a clean, production-oriented structure to ensure scalability and maintainability.

```bash
NLP Based Emotion Detection System
├── app/
│   └── main.py              # Streamlit web application
├── src/                     # Core logic package
│   ├── config.py            # Paths and global settings
│   ├── preprocess.py        # Text cleaning and normalization
│   ├── file_processor.py    # CSV, TXT, PDF, DOCX handlers
│   ├── model_loader.py      # Model loading with caching
│   ├── predictor.py         # Emotion prediction logic
│   ├── visualizer.py        # Confidence charts and colors
│   └── __init__.py          # Package exports
├── models/                  # Serialized models and vectorizer
├── notebooks/               # EDA and Model Training workflows
├── data/                    # Raw datasets (local only)
├── requirements.txt         # Dependency manifest
└── README.md
```

-----

## Getting Started

### 1. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-repo/emotion-detection-nlp.git
cd emotion-detection-nlp
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download NLTK Data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### 3. Launch the Web App

```bash
streamlit run app/main.py
```

### 4. Batch Processing

Upload CSV, TXT, PDF, or DOCX files through the web interface for bulk analysis.

**CSV Format Required:**
```csv
text
I am very happy today
This makes me angry
I love this weather
```

**TXT Format:** Each line treated as a separate sentence

**PDF/DOCX:** Text automatically extracted and processed

-----

## Model Performance

We evaluated three primary algorithms. The **XGBoost** model is recommended due to its superior F1-Score across all emotion classes.

| Model | Accuracy | F1-Macro | Balanced Acc |
| --- | --- | --- | --- |
| XGBoost | 89.7% | 87.3% | 87.7% |
| Logistic Regression | 89.8% | 86.1% | 84.9% |
| Linear SVM | 89.4% | 85.4% | 85.2% |

-----

## Dataset Insights

The models classify text into one of six emotion categories based on Bag-of-Words features extracted from 16,000+ sentences.

### Emotion Classes

| # | Emotion |
| --- | --- |
| 1 | Anger |
| 2 | Fear |
| 3 | Joy |
| 4 | Love |
| 5 | Sadness |
| 6 | Surprise |

### Feature Extraction

**Bag-of-Words (BoW) Configuration:**
- Max features: 7,000
- N-gram range: (1, 2)
- Min document frequency: 3
- Max document frequency: 0.7

**Preprocessing Pipeline:**
- Lowercase conversion
- Punctuation removal
- Number removal
- Extra space normalization

-----

## Outputs

- Predictions: Exported as CSV from batch processing
- Visualizations: Confidence distribution bar charts
- Logs: Streamlit console output for debugging

-----

## License & Attribution

**Author:** Shuban Ali

**License:** Distributed for educational use only.

-----

*Ready to detect emotions!*
```
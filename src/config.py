from pathlib import Path

# Project root directory (parent of src folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Directories
MODELS_DIR = PROJECT_ROOT / 'models'

# Model names and their files
MODEL_FILES = {
    'Logistic Regression': 'LogisticRegression_model.joblib',
    'Linear SVM': 'LinearSVC_model.joblib',
    'XGBoost': 'XGBoost_model.joblib'
}

# Vectorizer file
VECTORIZER_FILE = 'vectorizer_BoW.joblib'

# Encoder file
ENCODER_FILE = 'encoder.joblib'

# Emotion colors for visualization
EMOTION_COLORS = {
    'anger': '#FF4444',
    'fear': '#9B59B6',
    'joy': '#F1C40F',
    'love': '#FF6B8A',
    'sadness': '#3498DB',
    'surprise': '#2ECC71'
}

# Emotion emojis
EMOTION_EMOJIS = {
    'anger': '😠',
    'fear': '😨',
    'joy': '😊',
    'love': '❤️',
    'sadness': '😢',
    'surprise': '😲'
}
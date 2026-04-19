from .preprocess import clean_text

def predict_emotion(text, model, vectorizer, encoder):
    # Predict emotion from text
    cleaned = clean_text(text)
    
    if not cleaned:
        return None, 0, {}
    
    features = vectorizer.transform([cleaned])
    pred_label = model.predict(features)[0]
    
    if encoder:
        emotion = encoder.inverse_transform([pred_label])[0]
    else:
        emotions = {0: 'anger', 1: 'fear', 2: 'joy', 3: 'love', 4: 'sadness', 5: 'surprise'}
        emotion = emotions.get(pred_label, 'unknown')
    
    confidence = 0.0
    probabilities = {}
    
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(features)[0]
        confidence = float(max(probs))
        for i, p in enumerate(probs):
            emo_name = encoder.inverse_transform([i])[0]
            probabilities[emo_name] = float(p)
    else:
        confidence = 1.0
        probabilities[emotion] = 1.0
    
    return emotion, confidence, probabilities
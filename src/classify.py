import joblib

MODEL_PATH = "../models/classifier.pkl"

def classify_text(text: str) -> str:
    """Use trained ML model to classify text."""
    try:
        model = joblib.load(MODEL_PATH)
        return model.predict([text])[0]
    except Exception as e:
        print(f"[ERROR] Could not load model: {e}")
        return "Other"


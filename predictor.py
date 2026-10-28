"""
Fruit Quality Prediction Module
Compatible with TensorFlow 2.21.0+
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class FruitPredictor:

    def __init__(self):
        print("Loading model...")
        self.model = load_model("models/best_model.keras")

        self.class_names = [
            "Fresh Apple",
            "Fresh Banana",
            "Fresh Orange",
            "Rotten Apple",
            "Rotten Banana",
            "Rotten Orange"
        ]

        print("[OK] Model loaded successfully!")

    def predict_image(self, image_path):

        print(f"\nPredicting: {image_path}")

        # Load image
        img = image.load_img(image_path, target_size=(224, 224))

        # Convert to array
        img_array = image.img_to_array(img)

        # Expand dimensions
        img_array = np.expand_dims(img_array, axis=0)

        # Normalize
        img_array = img_array.astype("float32") / 255.0

        # Predict
        predictions = self.model.predict(img_array, verbose=0)

        predicted_index = int(np.argmax(predictions))

        confidence = float(np.max(predictions) * 100)

        predicted_class = self.class_names[predicted_index]

        status, fruit_type = predicted_class.split(" ", 1)

        result = {
            "success": True,
            "prediction": str(predicted_class),
            "fruit_type": str(fruit_type),
            "status": str(status),
            "confidence": round(confidence, 2),
            "confidence_raw": float(confidence / 100),
            "predicted_index": int(predicted_index),
            "suggestion": self.get_suggestion(predicted_class),
            "raw_predictions": [float(x) for x in predictions[0]]
        }

        print("\nPrediction Probabilities")

        for label, prob in zip(self.class_names, predictions[0]):
            print(f"{label:15} : {float(prob)*100:.2f}%")

        print("\nPrediction :", predicted_class)
        print("Confidence :", round(confidence, 2), "%")

        return result

    def get_suggestion(self, prediction):

        suggestions = {
            "Fresh Apple":
                "This apple looks fresh! Store in a cool, dry place.",
            "Fresh Banana":
                "This banana is fresh and ready to eat.",
            "Fresh Orange":
                "This orange is fresh and can be stored for several days.",
            "Rotten Apple":
                "This apple appears rotten. Do not consume it.",
            "Rotten Banana":
                "This banana appears rotten or overripe.",
            "Rotten Orange":
                "This orange appears rotten. Discard safely."
        }

        return suggestions.get(
            prediction,
            "Inspect the fruit carefully before consumption."
        )

    def is_ready(self):
        return self.model is not None


# Singleton Predictor
_predictor = None


def get_predictor():
    global _predictor

    if _predictor is None:
        _predictor = FruitPredictor()

    return _predictor


def predict_image(image_path):
    predictor = get_predictor()
    return predictor.predict_image(image_path)
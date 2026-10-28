"""
Mock Predictor for Testing Pipeline Logic

This module provides a mock predictor that simulates the ML model behavior
to test the pipeline logic without requiring a working model file.
"""

import os
import numpy as np
import hashlib
from tensorflow.keras.preprocessing import image

class MockFruitPredictor:
    """
    Mock predictor that simulates model behavior deterministically
    based on image content for testing purposes.
    """
    
    def __init__(self):
        """Initialize the mock predictor"""
        self.model = "mock_model"  # Placeholder
        self.class_labels = [
            "Fresh Apple",
            "Fresh Banana", 
            "Fresh Orange",
            "Rotten Apple",
            "Rotten Banana",
            "Rotten Orange"
        ]
        print(" Mock predictor initialized (for testing pipeline logic)")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image using the EXACT same pipeline as the standalone script.
        """
        try:
            print(f" Preprocessing image: {image_path}")
            
            # Use tensorflow.keras.preprocessing.image (same as standalone script)
            img = image.load_img(image_path, target_size=(224, 224))
            print(f" Image loaded with target size (224, 224)")
            
            # Convert image to array
            img_array = image.img_to_array(img)
            print(f" Image converted to array, shape: {img_array.shape}")
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            print(f" Batch dimension added, shape: {img_array.shape}")
            
            # Normalize (same as standalone script)
            img_array = img_array / 255.0
            print(f" Image normalized, min: {img_array.min():.6f}, max: {img_array.max():.6f}")
            
            return img_array
            
        except Exception as e:
            print(f" Error preprocessing image {image_path}: {str(e)}")
            raise
    
    def predict_image(self, image_path):
        """
        Mock prediction that produces deterministic results based on image content.
        """
        print(f"\n Starting MOCK prediction for: {image_path}")
        print("=" * 50)
        
        try:
            # Preprocess image using exact same pipeline
            processed_img = self.preprocess_image(image_path)
            
            # Generate deterministic "prediction" based on image content
            print(" Running MOCK model prediction...")
            
            # Create a deterministic hash of the image data
            image_hash = hashlib.md5(processed_img.tobytes()).hexdigest()
            print(f" Image hash (for determinism): {image_hash[:16]}...")
            
            # Convert hash to deterministic prediction
            hash_int = int(image_hash[:8], 16)  # Use first 8 hex chars
            
            # Create mock predictions that sum to 1.0
            np.random.seed(hash_int % 2**31)  # Seed for determinism
            raw_predictions = np.random.dirichlet(np.ones(6), 1)[0]  # 6 classes
            
            # Make one class clearly dominant for realistic results
            dominant_class = hash_int % 6
            raw_predictions[dominant_class] += 0.5
            raw_predictions = raw_predictions / raw_predictions.sum()  # Normalize
            
            print(" Mock prediction probabilities:")
            for i, (label, prob) in enumerate(zip(self.class_labels, raw_predictions)):
                print(f"  {i}: {label:<15} = {prob:.6f} ({prob*100:.2f}%)")
            
            # Get predicted class
            predicted_class_idx = np.argmax(raw_predictions)
            confidence = float(raw_predictions[predicted_class_idx])
            predicted_class = self.class_labels[predicted_class_idx]
            
            print(f"\n Mock prediction result:")
            print(f"  Predicted class index: {predicted_class_idx}")
            print(f"  Predicted class name: {predicted_class}")
            print(f"  Confidence score: {confidence:.6f} ({confidence*100:.2f}%)")
            
            # Parse fruit type and status
            parts = predicted_class.split(' ', 1)
            if len(parts) == 2:
                status = parts[0]      # Fresh, Rotten
                fruit_type = parts[1]  # Apple, Banana, Orange
            else:
                status = "Unknown"
                fruit_type = predicted_class
            
            # Get suggestion
            suggestion = self._get_suggestion(predicted_class, confidence)
            
            result = {
                'success': True,
                'prediction': predicted_class,
                'fruit_type': fruit_type,
                'status': status,
                'confidence': round(confidence * 100, 2),
                'confidence_raw': confidence,
                'predicted_index': int(predicted_class_idx),
                'suggestion': suggestion,
                'raw_predictions': raw_predictions.tolist(),
                'mock_mode': True,  # Indicate this is mock data
                'image_hash': image_hash[:16]  # For debugging
            }
            
            print(f" Mock prediction completed successfully")
            print("=" * 50)
            
            return result
            
        except Exception as e:
            print(f" Error during mock prediction: {str(e)}")
            raise
    
    def _get_suggestion(self, prediction, confidence):
        """Get suggestions based on prediction results."""
        suggestions = {
            'Fresh Apple': "This apple looks fresh! Store in a cool, dry place. Best consumed within a week.",
            'Fresh Banana': "This banana is fresh and ready to eat! Best consumed within 2-3 days.",
            'Fresh Orange': "This orange is fresh! Store at room temperature or refrigerate. Good for up to 2 weeks.",
            'Rotten Apple': "This apple appears rotten. Discard immediately to prevent contamination.",
            'Rotten Banana': "This banana is overripe/rotten. Consider composting or discard safely.",
            'Rotten Orange': "This orange appears rotten. Discard to prevent mold spread."
        }
        
        base_suggestion = suggestions.get(prediction, "Check the fruit carefully before consumption.")
        base_suggestion += " [MOCK PREDICTION - For testing only]"
        
        return base_suggestion
    
    def is_ready(self):
        """Check if the mock predictor is ready"""
        return True

# Create a function to get mock predictor for testing
def get_mock_predictor():
    """Get mock predictor instance for testing"""
    return MockFruitPredictor()

def mock_predict_image(image_path):
    """Convenience function for mock predictions"""
    predictor = get_mock_predictor()
    return predictor.predict_image(image_path)

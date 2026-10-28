#!/usr/bin/env python3
"""
Determinism Test Script

This script tests whether the prediction pipeline produces consistent results
for the same image across multiple runs.
"""

import os
import sys
import shutil
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from predictor import FruitPredictor

def test_determinism(image_path, num_tests=5):
    """
    Test prediction determinism by running the same image multiple times.
    
    Args:
        image_path (str): Path to test image
        num_tests (int): Number of test runs
    """
    print(f"🧪 Testing prediction determinism")
    print(f"📸 Image: {image_path}")
    print(f"🔄 Number of tests: {num_tests}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        return False
    
    try:
        # Initialize predictor
        predictor = FruitPredictor()
        
        if not predictor.is_ready():
            print("❌ Predictor not ready")
            return False
        
        results = []
        
        for i in range(num_tests):
            print(f"\n🔄 Test run #{i+1}")
            print("-" * 30)
            
            try:
                result = predictor.predict_image(image_path)
                
                # Extract key values for comparison
                test_result = {
                    'prediction': result['prediction'],
                    'confidence_raw': result['confidence_raw'],
                    'predicted_index': result['predicted_index'],
                    'raw_predictions': result['raw_predictions']
                }
                
                results.append(test_result)
                
                print(f"  Prediction: {result['prediction']}")
                print(f"  Confidence: {result['confidence']}% (raw: {result['confidence_raw']:.6f})")
                print(f"  Index: {result['predicted_index']}")
                
            except Exception as e:
                print(f"❌ Test run #{i+1} failed: {str(e)}")
                return False
        
        # Analyze results
        print("\n" + "=" * 60)
        print("📊 DETERMINISM ANALYSIS")
        print("=" * 60)
        
        # Check if all predictions are identical
        first_prediction = results[0]['prediction']
        first_confidence = results[0]['confidence_raw']
        first_index = results[0]['predicted_index']
        
        predictions_match = all(r['prediction'] == first_prediction for r in results)
        indices_match = all(r['predicted_index'] == first_index for r in results)
        
        print(f"📈 Predictions consistent: {'✅ YES' if predictions_match else '❌ NO'}")
        print(f"📈 Indices consistent: {'✅ YES' if indices_match else '❌ NO'}")
        
        # Check confidence score consistency (allowing tiny floating point differences)
        confidence_tolerance = 1e-10
        confidences_match = all(
            abs(r['confidence_raw'] - first_confidence) < confidence_tolerance 
            for r in results
        )
        print(f"📈 Confidence scores consistent: {'✅ YES' if confidences_match else '❌ NO'}")
        
        if not confidences_match:
            print("   Confidence values:")
            for i, r in enumerate(results):
                diff = abs(r['confidence_raw'] - first_confidence)
                print(f"     Run {i+1}: {r['confidence_raw']:.10f} (diff: {diff:.2e})")
        
        # Check raw predictions consistency
        raw_predictions_match = True
        for i, result in enumerate(results[1:], 1):
            for j in range(len(result['raw_predictions'])):
                diff = abs(result['raw_predictions'][j] - results[0]['raw_predictions'][j])
                if diff > confidence_tolerance:
                    raw_predictions_match = False
                    print(f"❌ Raw prediction mismatch in run {i+1}, class {j}: diff={diff:.2e}")
        
        if raw_predictions_match:
            print("📈 Raw predictions consistent: ✅ YES")
        
        # Summary
        all_consistent = predictions_match and indices_match and confidences_match and raw_predictions_match
        
        print("\n" + "=" * 60)
        if all_consistent:
            print("🎉 DETERMINISM TEST PASSED!")
            print("   All predictions are perfectly consistent across runs.")
        else:
            print("❌ DETERMINISM TEST FAILED!")
            print("   Predictions are inconsistent - there's a bug in the pipeline.")
        print("=" * 60)
        
        return all_consistent
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

def find_test_images():
    """Find available test images in the project"""
    possible_paths = [
        'static/uploads',  # Uploaded images
        'dataset/processed/test',  # Test dataset
        'dataset/raw'  # Raw dataset
    ]
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    found_images = []
    
    for base_path in possible_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if Path(file).suffix.lower() in image_extensions:
                        full_path = os.path.join(root, file)
                        found_images.append(full_path)
    
    return found_images

def main():
    """Main test function"""
    print("🔬 FRUIT PREDICTION DETERMINISM TEST")
    print("=" * 60)
    
    # Check if a specific image was provided
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
        if not os.path.exists(test_image):
            print(f"❌ Specified test image not found: {test_image}")
            return False
    else:
        # Find available test images
        print("🔍 Searching for test images...")
        available_images = find_test_images()
        
        if not available_images:
            print("❌ No test images found!")
            print("   Please provide an image path as argument:")
            print("   python test_determinism.py path/to/image.jpg")
            return False
        
        # Use the first available image
        test_image = available_images[0]
        print(f"📸 Using test image: {test_image}")
        
        if len(available_images) > 1:
            print(f"   (Found {len(available_images)} total images, using first one)")
    
    # Run the determinism test
    success = test_determinism(test_image, num_tests=5)
    
    if success:
        print("\n✅ All tests passed! The prediction pipeline is deterministic.")
    else:
        print("\n❌ Tests failed! The prediction pipeline has consistency issues.")
        print("\nDebugging tips:")
        print("1. Check that only one model is loaded")
        print("2. Verify preprocessing is identical to standalone script") 
        print("3. Ensure no random number generation in prediction")
        print("4. Check for threading or async issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
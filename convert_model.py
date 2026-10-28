#!/usr/bin/env python3
"""
Model Conversion Script

This script attempts to convert existing Keras models to formats compatible
with the current TensorFlow version.
"""

import os
import sys
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

def convert_model(input_path, output_path=None, output_format='h5'):
    """
    Convert model to compatible format.
    
    Args:
        input_path (str): Path to input model
        output_path (str): Path for converted model (optional)
        output_format (str): Output format ('h5', 'savedmodel', 'keras')
    """
    print(f" Converting model: {input_path}")
    print(f" Output format: {output_format}")
    
    if not os.path.exists(input_path):
        print(f" Input model not found: {input_path}")
        return False
    
    if output_path is None:
        name, ext = os.path.splitext(input_path)
        if output_format == 'h5':
            output_path = f"{name}_converted.h5"
        elif output_format == 'savedmodel':
            output_path = f"{name}_savedmodel"
        else:
            output_path = f"{name}_converted.keras"
    
    try:
        print(" Loading original model...")
        
        # Try different loading methods
        model = None
        loading_methods = [
            lambda: load_model(input_path),
            lambda: load_model(input_path, compile=False),
            lambda: load_model(input_path, custom_objects=tf.keras.utils.get_custom_objects()),
        ]
        
        for i, method in enumerate(loading_methods):
            try:
                print(f"  Attempt {i+1}: ", end="")
                model = method()
                print(" Success")
                break
            except Exception as e:
                print(f" Failed: {str(e)[:100]}...")
        
        if model is None:
            print(" Could not load model with any method")
            return False
        
        print(" Model loaded successfully")
        
        # Validate model
        print(" Validating model...")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
        print(f"  Parameters: {model.count_params():,}")
        
        # Test prediction
        print(" Testing model prediction...")
        test_input = np.random.random((1, 224, 224, 3))
        test_output = model.predict(test_input, verbose=0)
        print(f"  Test output shape: {test_output.shape}")
        print(f"  Test output sum: {test_output.sum():.6f}")
        
        # Save in new format
        print(f" Saving converted model to: {output_path}")
        
        if output_format == 'h5':
            model.save(output_path, save_format='h5')
        elif output_format == 'savedmodel':
            tf.saved_model.save(model, output_path)
        else:
            model.save(output_path, save_format='keras')
        
        print(" Model converted successfully!")
        
        # Verify converted model
        print(" Verifying converted model...")
        if output_format == 'savedmodel':
            loaded_model = tf.saved_model.load(output_path)
        else:
            loaded_model = load_model(output_path)
            
        # Test converted model
        if hasattr(loaded_model, 'predict'):
            verify_output = loaded_model.predict(test_input, verbose=0)
        else:
            # For SavedModel format
            infer = loaded_model.signatures['serving_default']
            verify_output = infer(tf.constant(test_input))
            verify_output = list(verify_output.values())[0].numpy()
        
        # Compare outputs
        if hasattr(loaded_model, 'predict'):
            diff = np.abs(test_output - verify_output).max()
            print(f"  Max difference: {diff:.10f}")
            if diff < 1e-6:
                print(" Converted model produces identical results")
            else:
                print(" Small differences in output (may be acceptable)")
        
        return True
        
    except Exception as e:
        print(f" Conversion failed: {str(e)}")
        return False

def main():
    """Main conversion function"""
    print(" KERAS MODEL CONVERSION TOOL")
    print("=" * 50)
    
    # Default models to convert
    models_to_convert = [
        'models/best_model.keras',
        'models/fruit_mobilenetv2.keras'
    ]
    
    # Check command line arguments
    if len(sys.argv) > 1:
        models_to_convert = [sys.argv[1]]
    
    output_format = 'h5'  # Default to .h5 for better compatibility
    if len(sys.argv) > 2:
        output_format = sys.argv[2]
    
    success_count = 0
    
    for model_path in models_to_convert:
        print(f"\n Processing: {model_path}")
        print("-" * 40)
        
        if convert_model(model_path, output_format=output_format):
            success_count += 1
        else:
            print(f" Failed to convert: {model_path}")
    
    print(f"\n" + "=" * 50)
    print(f" CONVERSION SUMMARY")
    print(f" Successful: {success_count}/{len(models_to_convert)}")
    
    if success_count > 0:
        print(f"\n Next steps:")
        print(f"1. Test the converted models:")
        print(f"   python test_determinism.py")
        print(f"2. Update predictor.py to use converted models")
        print(f"3. Run the Flask application")
    
    return success_count == len(models_to_convert)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

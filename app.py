import os
import sys
import hashlib
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import our predictor module (uses exact same approach as standalone script)
from predictor import predict_image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

print("[INFO] Initializing Fruit Quality Detection Application...")
print("[INFO] Using TensorFlow environment...")

# Test that the predictor works (same as standalone script)
try:
    from predictor import get_predictor
    predictor = get_predictor()
    print("[OK] Predictor initialized successfully!")
    print("[OK] Application ready to start!")
except Exception as e:
    print(f"[ERROR] Failed to initialize predictor: {str(e)}")
    print("[ERROR] Application cannot start without the working model.")
    exit(1)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """
    Generate a unique filename to prevent conflicts and ensure fresh uploads.
    This helps prevent caching issues.
    """
    timestamp = str(int(time.time() * 1000))  # milliseconds
    name, ext = os.path.splitext(original_filename)
    # Create a hash of the original name for uniqueness
    name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
    return f"{name_hash}_{timestamp}{ext}"

def validate_uploaded_file(filepath):
    """
    Validate that the uploaded file is a proper image and wasn't corrupted during upload.
    """
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            img.verify()  # Verify it's a valid image
        return True
    except Exception as e:
        print(f" File validation failed: {str(e)}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print("\n NEW PREDICTION REQUEST")
        print("=" * 60)
        
        if 'file' not in request.files:
            print(" No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print(" Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print(f" Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.'}), 400
        
        try:
            # Generate unique filename to prevent caching issues
            unique_filename = generate_unique_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            print(f" Original filename: {file.filename}")
            print(f" Unique filename: {unique_filename}")
            print(f" Full filepath: {filepath}")
            
            # Save the file
            file.save(filepath)
            print(f" File saved successfully")
            
            # Validate the uploaded file
            if not validate_uploaded_file(filepath):
                print(" File validation failed")
                try:
                    os.remove(filepath)
                except:
                    pass
                return jsonify({'error': 'Invalid or corrupted image file'}), 400
            
            print(" File validation passed")
            
            # Get file size for logging
            file_size = os.path.getsize(filepath)
            print(f"[INFO] File size: {file_size} bytes ({file_size/1024:.1f} KB)")
            
            # Make prediction using the REAL predictor (same as standalone script)
            print(f" Starting REAL prediction process...")
            
            try:
                result = predict_image(filepath)
                
                # Add additional metadata
                result.update({
                    'image_url': url_for('static', filename=f'uploads/{unique_filename}'),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'filename': unique_filename,
                    'original_filename': file.filename,
                    'file_size': file_size
                })
                
                print(f" REAL Prediction successful!")
                print(f" Result: {result['prediction']} ({result['confidence']}%)")
                print("=" * 60)
                
                return jsonify(result)
                
            except Exception as e:
                print(f" Prediction failed: {str(e)}")
                # Clean up file on prediction error
                try:
                    os.remove(filepath)
                except:
                    pass
                return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
                
        except Exception as e:
            print(f" File handling error: {str(e)}")
            return jsonify({'error': f'File processing error: {str(e)}'}), 500
    
    return render_template("predict.html")



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/health")
def health_check():
    """Health check endpoint to verify predictor status"""
    try:
        from predictor import get_predictor
        predictor = get_predictor()
        if predictor.is_ready():
            return jsonify({
                'status': 'healthy',
                'model_loaded': True,
                'model_path': 'models/best_model.keras',
                'environment': 'TensorFlow 2.21.0',
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'model_loaded': False,
                'error': 'Model not loaded',
                'timestamp': datetime.now().isoformat()
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'model_loaded': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(413)
def too_large(e):
    print(f" File too large error: {str(e)}")
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    print(f" Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True)

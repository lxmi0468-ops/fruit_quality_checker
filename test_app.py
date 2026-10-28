#!/usr/bin/env python3
"""
Test script to verify the Flask application setup and basic functionality
"""

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def check_file_structure():
    """Check if all required files and directories exist"""
    print("🔍 Checking project structure...")
    
    required_files = [
        'app.py',
        'templates/base.html',
        'templates/index.html',
        'templates/predict.html',
        'templates/about.html',
        'templates/contact.html',
        'templates/404.html',
        'static/css/style.css',
        'static/js/script.js',
        'README.md',
        'requirements.txt'
    ]
    
    required_dirs = [
        'models',
        'static/uploads',
        'templates',
        'static/css',
        'static/js',
        'static/images'
    ]
    
    # Check files
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    # Check directories
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}/")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
    
    if missing_dirs:
        print("\n❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}/")
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        'flask',
        'tensorflow',
        'PIL',
        'numpy',
        'cv2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
                print(f"  ✅ Pillow (PIL)")
            elif package == 'cv2':
                import cv2
                print(f"  ✅ opencv-python")
            else:
                __import__(package)
                print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
    
    return len(missing_packages) == 0

def check_models():
    """Check if ML model files exist"""
    print("\n🔍 Checking ML models...")
    
    model_files = [
        'models/best_model.keras',
        'models/fruit_mobilenetv2.keras'
    ]
    
    existing_models = []
    
    for model_path in model_files:
        if os.path.exists(model_path):
            size = os.path.getsize(model_path) / (1024 * 1024)  # Size in MB
            print(f"  ✅ {model_path} ({size:.1f} MB)")
            existing_models.append(model_path)
        else:
            print(f"  ❌ {model_path}")
    
    return len(existing_models) > 0

def test_flask_app():
    """Test basic Flask app functionality"""
    print("\n🔍 Testing Flask application...")
    
    try:
        from app import app
        print("  ✅ Flask app imported successfully")
        
        # Test app configuration
        with app.app_context():
            print(f"  ✅ Upload folder: {app.config.get('UPLOAD_FOLDER', 'Not set')}")
            print(f"  ✅ Max content length: {app.config.get('MAX_CONTENT_LENGTH', 'Not set')}")
        
        # Test routes
        with app.test_client() as client:
            routes_to_test = [
                ('/', 'Homepage'),
                ('/predict', 'Predict page'),
                ('/about', 'About page'),
                ('/contact', 'Contact page')
            ]
            
            for route, name in routes_to_test:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"  ✅ {name} ({route}) - Status: {response.status_code}")
                else:
                    print(f"  ❌ {name} ({route}) - Status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Flask app test failed: {str(e)}")
        return False

def check_static_files():
    """Check if static files are properly structured"""
    print("\n🔍 Checking static files...")
    
    css_file = 'static/css/style.css'
    js_file = 'static/js/script.js'
    
    success = True
    
    if os.path.exists(css_file):
        size = os.path.getsize(css_file) / 1024  # Size in KB
        print(f"  ✅ CSS file exists ({size:.1f} KB)")
    else:
        print(f"  ❌ CSS file missing")
        success = False
    
    if os.path.exists(js_file):
        size = os.path.getsize(js_file) / 1024  # Size in KB
        print(f"  ✅ JS file exists ({size:.1f} KB)")
    else:
        print(f"  ❌ JS file missing")
        success = False
    
    # Check if uploads directory is writable
    uploads_dir = 'static/uploads'
    try:
        os.makedirs(uploads_dir, exist_ok=True)
        test_file = os.path.join(uploads_dir, 'test_write.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"  ✅ Uploads directory is writable")
    except Exception as e:
        print(f"  ❌ Uploads directory not writable: {e}")
        success = False
    
    return success

def main():
    """Run all tests"""
    print("🚀 Testing Fruit Quality Detection Application")
    print("=" * 50)
    
    tests = [
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("ML Models", check_models),
        ("Static Files", check_static_files),
        ("Flask App", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your application is ready to run.")
        print("Start the server with: python app.py")
        print("Then visit: http://127.0.0.1:5000/")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
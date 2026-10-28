# 🍎 Fruit Quality Detection using Deep Learning

An AI-powered web application that detects the freshness and quality of fruits by classifying them as **Fresh** or **Rotten** using **MobileNetV2** transfer learning deployed on **Flask**.

---

## 📑 Table of Contents
1. [Overview](#overview)
2. [Supported Fruits & Classes](#supported-fruits--classes)
3. [Errors Fixed](#-errors-fixed)
4. [How to Run the Project](#-how-to-run-the-project)
5. [How to Work This Project: Tab-by-Tab Guide](#-how-to-work-this-project-tab-by-tab-guide)
   - [Tab 1: Home (`/`)](#tab-1-home-)
   - [Tab 2: Predict (`/predict`) - Main Work Tab](#tab-2-predict-predict---the-main-working-tab)
   - [Tab 3: About (`/about`)](#tab-3-about-about)
   - [Tab 4: Contact (`/contact`)](#tab-4-contact-contact)
6. [API & Health Endpoints](#-api--health-endpoints)
7. [Running Verification Tests](#-running-verification-tests)
8. [Project Structure](#project-structure)

---

## Overview

This project uses a trained **MobileNetV2** deep learning model to inspect fruit images and classify their quality with high precision.

- **Model Accuracy**: **98.26%**
- **Inference Pipeline**: 100% Deterministic & consistent predictions
- **Web Interface**: Modern responsive UI with real-time feedback
- **Backend**: Flask API with image validation and caching protection

---

## Supported Fruits & Classes

The model classifies images into **6 categories**:

| Fruit | Fresh Class | Rotten Class |
|---|---|---|
| **Apple** 🍎 | `Fresh Apple` | `Rotten Apple` |
| **Banana** 🍌 | `Fresh Banana` | `Rotten Banana` |
| **Orange** 🍊 | `Fresh Orange` | `Rotten Orange` |

---

## 🛠️ Errors Fixed

During system verification, the following issues were identified and resolved:

1. **Missing TensorFlow Installation**:
   - `ModuleNotFoundError: No module named 'tensorflow'` occurred when starting the project.
   - **Fix**: Installed compatible TensorFlow (`tensorflow 2.22+` / `keras`) in the environment.

2. **Windows Console UnicodeEncodeError (`cp1252`)**:
   - Python threw `UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'` and `'\U0001F4CF'` in [predictor.py](file:///c:/fruit-quality-detection-main/predictor.py) and [app.py](file:///c:/fruit-quality-detection-main/app.py) because Windows console defaults to cp1252.
   - **Fix**: Replaced raw Unicode emojis with standard tags (`[OK]`, `[INFO]`) and configured `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`.

3. **Missing `/about` Route**:
   - The navigation bar linked to `/about`, and `templates/about.html` existed, but [app.py](file:///c:/fruit-quality-detection-main/app.py) had no `@app.route("/about")` handler, causing a 404 error when clicking the About tab.
   - **Fix**: Added `@app.route("/about")` in [app.py](file:///c:/fruit-quality-detection-main/app.py).

4. **Missing `static/uploads/` Directory**:
   - Upload directory was absent on cold start, causing [test_app.py](file:///c:/fruit-quality-detection-main/test_app.py) file-structure validation to fail.
   - **Fix**: Created directory and verified upload write permissions.

---

## 🚀 How to Run the Project

### 1. Open Terminal / PowerShell
Navigate to the project folder:
```powershell
cd c:\fruit-quality-detection-main
```

### 2. Verify or Install Dependencies
Ensure dependencies are installed:
```powershell
pip install tensorflow flask pillow opencv-python numpy werkzeug
```

### 3. Run the Flask Server
```powershell
python app.py
```
You will see output indicating that the model loaded successfully:
```text
[INFO] Initializing Fruit Quality Detection Application...
[INFO] Using TensorFlow environment...
Loading model...
[OK] Model loaded successfully!
[OK] Predictor initialized successfully!
[OK] Application ready to start!
 * Running on http://127.0.0.1:5000
```

### 4. Open in Your Web Browser
Open your browser (Chrome, Edge, Firefox, Brave) and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧭 How to Work This Project: Tab-by-Tab Guide

The web application contains a top navigation bar with **4 tabs**:

```
[ FruitAI ]        Home  |  Predict  |  About  |  Contact
```

### Tab 1: Home (`/`)
- **What it is**: The landing page of the application.
- **What you see**:
  - Hero header introducing the fruit quality detection system.
  - Quick-start guide ("How to Use" bullet points).
  - Feature highlights (Fast Prediction, MobileNetV2 architecture, 98.26% accuracy).
  - Supported fruits showcase (Apple, Banana, Orange).
- **What to do here**:
  - Read the overview.
  - Click the **"Start Prediction"** button to jump directly to the prediction tab.

---

### Tab 2: Predict (`/predict`) - THE MAIN WORKING TAB
> 💡 **This is the core tab where all fruit freshness detection is performed.**

#### Step-by-Step Instructions:
1. **Navigate to the Predict tab**:
   - Click **"Predict"** in the top navigation bar or go to `http://127.0.0.1:5000/predict`.
2. **Select or Drag an Image**:
   - Either drag and drop an image file into the dashed drop area, or click the **"Browse Files"** button.
   - **Supported formats**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif` (up to 16MB).
   - Use a clear, well-lit photo of an **Apple**, **Banana**, or **Orange**.
3. **Review the Image Preview**:
   - Once selected, the image preview appears on screen.
   - If you picked the wrong file, click **"Remove Image"** to pick another one.
4. **Click "Analyze Fruit Quality"**:
   - Click the green **"Analyze Fruit Quality"** button.
   - A loading indicator will briefly display while the deep learning model analyzes the image.
5. **Read the Output Results**:
   The prediction card will display:
   - **Freshness Status**: A badge showing `Fresh` (green checkmark) or `Rotten` (red cross mark).
   - **Predicted Class**: E.g., `Fresh Apple`, `Rotten Banana`, etc.
   - **Confidence Score**: A percentage (e.g. `98.5%`) with a visual confidence bar.
   - **Analysis Details**:
     - *Fruit Type*: Apple, Banana, or Orange.
     - *Status*: Fresh or Rotten.
     - *Timestamp*: Date and time of the analysis.
     - *Filename*: Unique cache-busted file reference.
   - **Actionable Recommendation**:
     - *Fresh Fruit*: Suggestions on how to store or consume it.
     - *Rotten Fruit*: Warning that the fruit is spoiled and unsafe to consume.
   - **Debug Info**: Expandable raw probability distribution across all 6 classes.
6. **Analyze More Fruits**:
   - Click the **"Analyze Another Fruit"** button to reset the uploader and test additional images.

---

### Tab 3: About (`/about`)
- **What it is**: Detailed documentation on the project background and technology.
- **What you see**:
  - **Project Overview**: Motivation for automated computer vision quality inspection.
  - **Problem Statement & Solution**: Reducing food waste and standardizing fruit sorting.
  - **Model Architecture**: Explanations of MobileNetV2, depthwise separable convolutions, and transfer learning.
  - **Performance Metrics**: Tables showing precision, recall, test accuracy (98.26%), and F1-score.
- **What to do here**:
  - Review technical details and academic research information about the deep learning pipeline.

---

### Tab 4: Contact (`/contact`)
- **What it is**: The communication and inquiry portal.
- **What you see**:
  - **Contact Details**: Institution, lab information, email addresses, and GitHub link.
  - **Project Statistics**: Quick summary counters (98.26% Accuracy, 6 Classes, 3 Fruits, Real-time).
  - **Message Form**: First name, last name, email, subject, and message fields.
  - **FAQ Section**: Accordion answering common questions (commercial licensing, dataset expansion, etc.).
- **What to do here**:
  - Submit inquiries or feedback through the message form.

---

## 📡 API & Health Endpoints

You can also interact with the project programmatically via HTTP:

### 1. Health Check
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"
```
**Response**:
```json
{
  "environment": "TensorFlow 2.21.0+",
  "model_loaded": true,
  "model_path": "models/best_model.keras",
  "status": "healthy",
  "timestamp": "2026-10-24T15:14:23.208660"
}
```

### 2. Predict via Command Line (cURL)
```powershell
curl.exe -F "file=@static/images/hero.png" http://127.0.0.1:5000/predict
```
**Response**:
```json
{
  "confidence": 57.67,
  "confidence_raw": 0.57665,
  "fruit_type": "Banana",
  "prediction": "Fresh Banana",
  "status": "Fresh",
  "suggestion": "This banana is fresh and ready to eat.",
  "success": true
}
```

---

## 🧪 Running Verification Tests

Run the included automated verification scripts to ensure everything is operating cleanly:

### 1. Run Complete Application Test Suite
```powershell
python test_app.py
```
*Validates file structure, Python dependencies, model weights, static files, and Flask routes (5/5 PASS).*

### 2. Run Pipeline Determinism Test
```powershell
python test_determinism.py static/images/hero.png
```
*Verifies that running multiple predictions on the same image yields 100% identical probabilities with zero drift.*

---

## Project Structure

```text
fruit-quality-detection-main/
│
├── app.py                      # Flask web application & API routes
├── predictor.py                # Deep learning prediction engine (MobileNetV2)
├── models/
│   ├── best_model.keras        # Trained Keras model weights
│   └── fruit_mobilenetv2.keras # MobileNetV2 architecture model
├── templates/
│   ├── base.html               # Shared layout & navigation header/footer
│   ├── index.html              # Home Tab (/)
│   ├── predict.html            # Predict Tab (/predict) - Main work tab
│   ├── about.html              # About Tab (/about)
│   ├── contact.html            # Contact Tab (/contact)
│   └── 404.html                # Error page
├── static/
│   ├── css/style.css           # Styling & animations
│   ├── js/script.js            # Frontend interactivity
│   ├── images/                 # Sample images & assets
│   └── uploads/                # Directory for uploaded user images
├── requirements.txt            # Python dependencies
├── test_app.py                 # Automated test suite
├── test_determinism.py         # Multi-run consistency test
└── README.md                   # Complete documentation & user guide
```

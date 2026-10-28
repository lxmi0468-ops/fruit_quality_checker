import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# Paths
# -----------------------------

MODEL_PATH = "models/best_model.keras"

TEST_PATH = r"D:\Projects\fruit_detection_project\archive\dataset\test"

RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)

# -----------------------------
# Load Model
# -----------------------------

print("Loading model...")
model = load_model(MODEL_PATH)

# -----------------------------
# Test Generator
# -----------------------------

IMG_SIZE = (224,224)
BATCH_SIZE = 32

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    TEST_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# -----------------------------
# Predict
# -----------------------------

print("\nPredicting on test images...")

predictions = model.predict(test_generator)

predicted_classes = np.argmax(predictions, axis=1)

true_classes = test_generator.classes

class_names = list(test_generator.class_indices.keys())

# -----------------------------
# Accuracy
# -----------------------------

accuracy = accuracy_score(true_classes, predicted_classes)

print("\n==============================")
print(f"Test Accuracy : {accuracy*100:.2f}%")
print("==============================")

# -----------------------------
# Classification Report
# -----------------------------

report = classification_report(
    true_classes,
    predicted_classes,
    target_names=class_names
)

print("\nClassification Report\n")
print(report)

with open(os.path.join(RESULTS_DIR,"classification_report.txt"),"w") as f:
    f.write(report)

# -----------------------------
# Confusion Matrix
# -----------------------------

cm = confusion_matrix(true_classes,predicted_classes)

plt.figure(figsize=(10,8))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.tight_layout()

plt.savefig(os.path.join(RESULTS_DIR,"confusion_matrix.png"))

plt.show()

print("\nConfusion matrix saved.")

# -----------------------------
# Confidence Distribution
# -----------------------------

confidence = np.max(predictions,axis=1)

plt.figure(figsize=(8,5))

plt.hist(confidence,bins=20)

plt.title("Prediction Confidence Distribution")

plt.xlabel("Confidence")

plt.ylabel("Number of Images")

plt.tight_layout()

plt.savefig(os.path.join(RESULTS_DIR,"confidence_distribution.png"))

plt.show()

print("Confidence graph saved.")

# -----------------------------
# Save Summary
# -----------------------------

with open(os.path.join(RESULTS_DIR,"summary.txt"),"w") as f:

    f.write(f"Accuracy : {accuracy*100:.2f}%\n")

    f.write(f"Total Test Images : {len(true_classes)}\n")

    f.write(f"Classes : {len(class_names)}\n")

print("\nEvaluation completed successfully.")
print(f"\nAll files are saved in : {RESULTS_DIR}")
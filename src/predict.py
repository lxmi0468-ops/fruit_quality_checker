import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained model
model = load_model("models/best_model.keras")

# Class names (must match train_generator.class_indices)
class_names = [
    "Fresh Apple",
    "Fresh Banana",
    "Fresh Orange",
    "Rotten Apple",
    "Rotten Banana",
    "Rotten Orange"
]

# Enter image path here
img_path = r"D:\fruit_detection_project\fresh_apple.jpg"
# Load image
img = image.load_img(img_path, target_size=(224, 224))

# Convert image to array
img_array = image.img_to_array(img)

# Add batch dimension
img_array = np.expand_dims(img_array, axis=0)

# Normalize
img_array = img_array / 255.0

# Predict
predictions = model.predict(img_array)

# Get predicted class index
predicted_index = np.argmax(predictions)

# Get confidence score
confidence = np.max(predictions) * 100

# Display results
print("\nPrediction Results")
print("------------------")
print("Predicted Class:", class_names[predicted_index])
print(f"Confidence: {confidence:.2f}%")
import cv2
import matplotlib.pyplot as plt

image_path = r"D:\fruit_detection_project\archive\dataset\train\freshapples\rotated_by_15_Screen Shot 2018-06-08 at 4.59.36 PM.png"

image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image = cv2.resize(image, (224, 224))

# Gaussian Blur
gaussian = cv2.GaussianBlur(image, (5, 5), 0)

# Median Blur
median = cv2.medianBlur(image, 5)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(image)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(gaussian)
plt.title("Gaussian Blur")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(median)
plt.title("Median Blur")
plt.axis("off")

plt.show()
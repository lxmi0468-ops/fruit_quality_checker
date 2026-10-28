import cv2
import matplotlib.pyplot as plt

image_path = r"D:\fruit_detection_project\archive\dataset\train\freshapples\rotated_by_15_Screen Shot 2018-06-08 at 4.59.36 PM.png"

image = cv2.imread(image_path)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

resized = cv2.resize(image_rgb, (224, 224))

print("Original Shape:", image_rgb.shape)
print("Resized Shape:", resized.shape)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(resized)
plt.title("224 x 224")
plt.axis("off")

plt.show()
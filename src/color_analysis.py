import cv2
import matplotlib.pyplot as plt

image_path = r"D:\fruit_detection_project\archive\dataset\train\freshapples\rotated_by_15_Screen Shot 2018-06-08 at 4.59.36 PM.png"

# Read image
image = cv2.imread(image_path)

# BGR → RGB
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# RGB → HSV
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

# Split channels
h, s, v = cv2.split(hsv)

plt.figure(figsize=(15,8))

plt.subplot(2,2,1)
plt.imshow(rgb)
plt.title("RGB Image")
plt.axis("off")

plt.subplot(2,2,2)
plt.imshow(h, cmap="hsv")
plt.title("Hue Channel")
plt.axis("off")

plt.subplot(2,2,3)
plt.imshow(s, cmap="gray")
plt.title("Saturation Channel")
plt.axis("off")

plt.subplot(2,2,4)
plt.imshow(v, cmap="gray")
plt.title("Value (Brightness)")
plt.axis("off")

plt.tight_layout()
plt.show()
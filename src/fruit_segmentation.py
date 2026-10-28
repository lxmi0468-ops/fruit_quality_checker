import cv2
import matplotlib.pyplot as plt

image_path = r"D:\fruit_detection_project\archive\dataset\train\freshapples\rotated_by_15_Screen Shot 2018-06-08 at 4.59.36 PM.png"

# Read image
image = cv2.imread(image_path)

# Convert to RGB
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Thresholding
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

largest_contour = max(contours, key=cv2.contourArea)

# Create mask
mask = gray.copy()
mask[:] = 0

cv2.drawContours(
    mask,
    [largest_contour],
    -1,
    255,
    thickness=cv2.FILLED
)

# Apply mask
segmented = cv2.bitwise_and(
    rgb,
    rgb,
    mask=mask
)

plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.imshow(rgb)
plt.title("Original")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(mask, cmap="gray")
plt.title("Mask")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(segmented)
plt.title("Segmented Fruit")
plt.axis("off")

plt.show()
import cv2
import matplotlib.pyplot as plt

image_path = r"D:\fruit_detection_project\archive\dataset\train\freshapples\rotated_by_15_Screen Shot 2018-06-08 at 4.59.36 PM.png"

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print("Image Shape:", image.shape)

plt.imshow(image_rgb)
plt.title("Fresh Apple")
plt.axis("off")
plt.show()
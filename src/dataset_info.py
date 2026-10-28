import os

dataset_path = r"D:\fruit_detection_project\archive\dataset\train"

classes = os.listdir(dataset_path)

print("Classes:")
print(classes)

total_images = 0

for cls in classes:
    class_path = os.path.join(dataset_path, cls)
    count = len(os.listdir(class_path))
    total_images += count

    print(f"{cls}: {count}")

print("\nTotal Images:", total_images)
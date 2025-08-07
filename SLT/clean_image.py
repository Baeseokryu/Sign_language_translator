from PIL import Image, UnidentifiedImageError
import os

folders = ['train', 'val']
base_path = 'C:/Users/Dell/priya/SLT/SLT'

corrupt_count = 0

for folder in folders:
    folder_path = os.path.join(base_path, folder)
    for class_name in os.listdir(folder_path):
        class_dir = os.path.join(folder_path, class_name)
        if not os.path.isdir(class_dir):
            continue

        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            try:
                with Image.open(img_path) as img:
                    img.convert("RGB").load()
            except Exception as e:
                print(f"❌ {img_path} - {e}")
                os.remove(img_path)
                corrupt_count += 1

print(f"✅ Cleanup done. Removed {corrupt_count} bad images.")

import os
import shutil
import random

source_dir = 'C:/Users/Dell/priya/SLT/SLT/ISL_DATASET'   # Your full ISL dataset path
target_dir = 'C:/Users/Dell/priya/SLT/SLT/ISL_subset'     # New subset folder

max_images_per_class = 200
os.makedirs(target_dir, exist_ok=True)

for cls in sorted(os.listdir(source_dir)):
    cls_path = os.path.join(source_dir, cls)
    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    random.shuffle(images)
    selected = images[:max_images_per_class]

    new_cls_path = os.path.join(target_dir, cls)
    os.makedirs(new_cls_path, exist_ok=True)

    for img in selected:
        shutil.copy(os.path.join(cls_path, img), os.path.join(new_cls_path, img))

    print(f"✅ {cls}: {len(selected)} images copied.")

print("\n🎉 Subset created at:", target_dir)

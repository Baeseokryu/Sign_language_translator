import os
import shutil
import random

subset_dir = 'C:/Users/Dell/priya/SLT/SLT/ISL_subset'  # Path to your subset
train_dir = 'C:/Users/Dell/priya/SLT/SLT/train'
val_dir = 'C:/Users/Dell/priya/SLT/SLT/val'

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for cls in os.listdir(subset_dir):
    cls_path = os.path.join(subset_dir, cls)
    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    random.shuffle(images)
    split = min(100, int(0.8 * len(images)))


    train_cls_path = os.path.join(train_dir, cls)
    val_cls_path = os.path.join(val_dir, cls)

    os.makedirs(train_cls_path, exist_ok=True)
    os.makedirs(val_cls_path, exist_ok=True)

    for img in images[:split]:
        shutil.copy(os.path.join(cls_path, img), os.path.join(train_cls_path, img))
    for img in images[split:]:
        shutil.copy(os.path.join(cls_path, img), os.path.join(val_cls_path, img))

    print(f"✅ {cls}: {split} train | {len(images)-split} val")

print("\n📂 Dataset successfully split into 'train/' and 'val/'")

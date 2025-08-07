import os

# 👇 Replace this with the correct path to your training data
train_dir = "C:/Users/Dell/priya/SLT/SLT/train"
if not os.path.exists(train_dir):
    print("Training directory not found!")
else:
    print("Class Distribution in Training Set:\n")

    for cls in sorted(os.listdir(train_dir)):
        cls_path = os.path.join(train_dir, cls)
        if os.path.isdir(cls_path):
            count = len([img for img in os.listdir(cls_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])
            print(f"{cls}: {count} images")

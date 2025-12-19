import base64
import os

icons = []
icon_dir = 'image'

# نرتب الملفات بالاسم باش الترتيب يبقى ثابت
for filename in sorted(os.listdir(icon_dir)):
    file_path = os.path.join(icon_dir, filename)
    with open(file_path, "rb") as f:
        icons.append(base64.b64encode(f.read()).decode('utf-8'))

# نعرض ترتيب الصور باش نتأكد
for i, name in enumerate(sorted(os.listdir(icon_dir))):
    print(i, name)
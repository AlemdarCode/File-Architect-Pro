
import os

files = ["vline.svg", "branch-end.svg", "branch-more.svg"]
base_dir = "icons"

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Replace black strokes/fills with white/light gray
        new_content = content.replace('stroke="black"', 'stroke="#E0E0E0"')
        new_content = new_content.replace('stroke="#000"', 'stroke="#E0E0E0"')
        new_content = new_content.replace('fill="black"', 'fill="#E0E0E0"')
        
        new_name = f.replace(".svg", "-white.svg")
        new_path = os.path.join(base_dir, new_name)
        
        with open(new_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Created {new_name}")

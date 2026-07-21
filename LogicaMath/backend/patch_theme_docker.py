import re
import os

files_to_patch = [
    "/app/app/fase5/seed.py",
    "/app/app/fase5/theory_examples.py",
    "/app/app/fase5/svg_helpers.py"
]

def patch_file(filepath):
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex replacements
    # 1. Update backgrounds from any dark or #0F172A to #111827 (or replace all background:#... with background:#111827)
    content = re.sub(r'background:\s*#[0-9a-fA-F]{6}', 'background:#111827', content)
    
    # 2. Update font-sizes to minimum 13
    # Look for font-size='XX' or font-size="XX" or font-size=XX
    def replace_font_size(match):
        prefix = match.group(1)
        quote1 = match.group(2) or ""
        size_str = match.group(3)
        suffix = match.group(4)
        
        try:
            size = int(size_str)
            if size < 13:
                size = 13
        except ValueError:
            pass
            
        return f"{prefix}{quote1}{size}{quote1}{suffix}"
    
    content = re.sub(r'(font-size=)([\'"]?)(\d+)([\'"]?)', replace_font_size, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Patched: {filepath}")

for fp in files_to_patch:
    patch_file(fp)

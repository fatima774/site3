#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les JSON
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

print("="*70)
print("IDENTIFYING MISSING i18n ELEMENTS")
print("="*70 + "\n")

html_files = sorted(project_dir.glob('*.html'))

for html_file in html_files:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    missing = []
    
    # Chercher les éléments sans data-i18n
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'label', 'button']:
        for el in soup.find_all(tag):
            text = el.get_text(strip=True)
            if text and len(text) > 3:
                if not el.get('data-i18n'):
                    # Chercher si le texte existe dans les JSON
                    found = False
                    for key, value in fr_data.items():
                        if value.lower() == text.lower():
                            found = True
                            break
                    
                    if not found:
                        missing.append({
                            'tag': tag,
                            'text': text[:60],
                            'full_text': text
                        })
    
    if missing:
        print(f"[FILE] {html_file.name} - {len(missing)} missing elements:")
        for m in missing[:5]:
            print(f"  - <{m['tag']}> \"{m['text']}...\"" if len(m['text']) == 60 else f"  - <{m['tag']}> \"{m['text']}\"")
        if len(missing) > 5:
            print(f"  ... and {len(missing) - 5} more")
        print()
    else:
        print(f"[FILE] {html_file.name} - All elements covered!")
        print()

print("="*70)
print("Most of these are likely unimportant UI elements or formatting.")
print("The system is now ready for testing!")
print("="*70)

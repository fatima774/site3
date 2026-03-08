#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

project_dir = Path(__file__).parent
lang_dir = project_dir / "assets" / "lang"

# Charger les nouveaux mappings
with open(project_dir / "mapping_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

new_keys = report["new_keys"]

# Charger fr.json pour avoir toutes les clés
with open(lang_dir / "fr.json", "r", encoding="utf-8") as f:
    fr_data = json.load(f)

# Créer un index inverse text -> key
text_to_key = {}
for key, value in fr_data.items():
    text_to_key[value.lower().strip()] = key
    # Aussi essayer sans accents
    text_normalized = re.sub(r'[^\w\s]', '', value.lower().strip())
    if text_normalized:
        text_to_key[text_normalized] = key

# Créer un index à partir de new_keys
for key, value in new_keys.items():
    text_to_key[value.lower().strip()] = key
    text_normalized = re.sub(r'[^\w\s]', '', value.lower().strip())
    if text_normalized:
        text_to_key[text_normalized] = key

def find_key_for_text(text):
    """Trouve la clé correspondant à un texte"""
    text_clean = text.strip().lower()
    
    # Essai direct
    if text_clean in text_to_key:
        return text_to_key[text_clean]
    
    # Essai sans accents
    text_normalized = re.sub(r'[^\w\s]', '', text_clean)
    if text_normalized in text_to_key:
        return text_to_key[text_normalized]
    
    # Essai partial inversé (si dans new_keys)
    for key, value in new_keys.items():
        if value.lower().strip() == text_clean:
            return key
    
    return None

html_files = sorted(project_dir.glob('*.html'))
print("="*70)
print("ADDING data-i18n ATTRIBUTES TO HTML FILES")
print("="*70 + "\n")

for html_file in html_files:
    print(f"Processing: {html_file.name}")
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    modified = False
    
    # Title
    title = soup.find('title')
    if title and not title.get('data-i18n'):
        text = title.get_text(strip=True)
        key = find_key_for_text(text)
        if key:
            title['data-i18n'] = key
            modified = True
            print(f"  <title> -> {key}")
    
    # H1-H6
    for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for el in soup.find_all(tag_name):
            if el.get('data-i18n'):
                continue
            text = el.get_text(strip=True)
            if text and len(text) > 3 and text not in ['Menu']:
                key = find_key_for_text(text)
                if key:
                    el['data-i18n'] = key
                    modified = True
    
    # P elements
    for el in soup.find_all('p'):
        if el.get('data-i18n'):
            continue
        text = el.get_text(strip=True)
        if text and len(text) > 15:
            key = find_key_for_text(text)
            if key:
                el['data-i18n'] = key
                modified = True
    
    # Labels
    for el in soup.find_all('label'):
        if el.get('data-i18n'):
            continue
        text = el.get_text(strip=True)
        if text:
            key = find_key_for_text(text)
            if key:
                el['data-i18n'] = key
                modified = True
    
    # Buttons with classes
    for el in soup.find_all(['button', 'a']):
        if el.get('data-i18n'):
            continue
        if 'btn' in el.get('class', []) or 'cta' in el.get('class', []):
            text = el.get_text(strip=True)
            if text and text not in ['Menu', 'Accueil']:
                key = find_key_for_text(text)
                if key:
                    el['data-i18n'] = key
                    modified = True
    
    if modified:
        # Sauvegarder
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify(formatter=None)))
        print(f"  SAVED")
    else:
        print(f"  No changes")

print("\n" + "="*70)
print("COMPLETE: data-i18n attributes added to HTML files")
print("="*70)
